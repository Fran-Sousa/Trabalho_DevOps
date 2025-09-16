"""Stack para a infra com AWS CDK."""

# from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_logs as logs
from constructs import Construct


class ToDoStack(Stack):
    """Stack da aplicação ToDo."""

    def __init__(
        self, scope: Construct, construct_id: str, *, image_tag: str, **kwargs
    ):
        """Inicializa a stack da aplicação ToDo."""
        super().__init__(scope, construct_id, **kwargs)

        # Criação de log group do CloudWatch
        log_group = logs.LogGroup(
            self,
            "ToDoLogGroup",
            log_group_name="/ecs/ToDo",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # VPC (2 AZs, suficiente para demo)
        vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
            restrict_default_security_group=False,
        )

        # Cluster ECS
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # ECR repo - criar se não existir
        '''repo = ecr.Repository(
            self,
            "TodoRepository",
            repository_name="todo",
            removal_policy=RemovalPolicy.DESTROY,
        )'''
        repo = ecr.Repository.from_repository_name(
            self, "repo", repository_name="todo"
        )

        print("Repo: " + str(repo))

        # Imagem com tag dinamico (passado pelo GitHub Actions
        # via -c imageTag=...)
        print("Image tag: " + image_tag)
        image = ecs.ContainerImage.from_ecr_repository(repo, tag=image_tag)
        print("Image: " + str(image))

        # Task Definition do ECS sem ALB (menor custo para nossa aula)
        task_def = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            cpu=256,
            memory_limit_mib=512,
        )
        container = task_def.add_container(
            "App",
            image=image,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix="ToDo", log_group=log_group
            ),
            environment={
                # adicione variáveis se precisar
            },
        )
        # Exponha a porta do seu FastAPI
        container.add_port_mappings(
            ecs.PortMapping(container_port=8000, protocol=ecs.Protocol.TCP)
        )
        # Security Group permitindo acesso externo à porta 8000
        sg = ec2.SecurityGroup(
            self, "FargateSG", vpc=vpc, allow_all_outbound=True
        )
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(8000),
            "Permitir HTTP (porta 8000) de qualquer lugar",
        )
        # Serviço Fargate SEM Load Balancer, com IP público
        svc = ecs.FargateService(
            self,
            "Service",
            cluster=cluster,
            task_definition=task_def,
            desired_count=1,
            assign_public_ip=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_groups=[sg],
            enable_execute_command=True,
        )

        # Output com instruções para obter a URL da API
        CfnOutput(
            self,
            "ApiUrlInstructions",
            value="Para obter a URL da API, execute: aws ecs describe-tasks --cluster {} --tasks $(aws ecs list-tasks --cluster {} --service-name {} --query 'taskArns[0]' --output text) --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text | xargs -I {{}} aws ec2 describe-network-interfaces --network-interface-ids {{}} --query 'NetworkInterfaces[0].Association.PublicIp' --output text".format(
                cluster.cluster_name, cluster.cluster_name, svc.service_name
            ),
            description="Comando para obter o IP público da API",
        )

        CfnOutput(
            self,
            "ApiPort",
            value="8000",
            description="Porta da API - URL será http://[IP_PUBLICO]:8000",
        )
