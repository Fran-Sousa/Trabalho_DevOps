#!/usr/bin/env python3
"""src/database/migrations.py Popula o banco com dados de exemplo."""
import os
import sys

from .db import Task, User, session

"""teste"""
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)


def create_sample_data():
    """Cria dados de exemplo."""
    print("Criando dados de exemplo...")

    try:
        # Verificar se já existem usuários
        existing_users = session.query(User).count()
        if existing_users > 0:
            print(f"Já existem {existing_users} usuários no banco")
            show_data()
            return

        # Criar usuários
        users = [
            User(name="Admin DevOps", username="admin", password="admin123"),
        ]

        for user in users:
            session.add(user)

        session.commit()
        print("Usuários criados!")

        # Criar tarefas
        admin = session.query(User).filter(User.username == "admin").first()

        tasks = [
            # TASK EXEMPLO
            Task(
                title="Configurar Docker",
                status="todo",
                priority="high",
                user_id=admin.id,
            ),
        ]

        for task in tasks:
            session.add(task)

        session.commit()
        print("Tarefas criadas!")

        show_data()

    except Exception as e:
        print(f"Erro: {e}")
        session.rollback()


def show_data():
    """Mostra dados do banco."""
    try:
        user_count = session.query(User).count()
        task_count = session.query(Task).count()
        """teste"""
        print("Resumo do banco:")
        print(f"Usuários: {user_count}")
        print(f"Tarefas: {task_count}")

        print("\nUsuários:")
        users = session.query(User).all()
        for user in users:
            tasks = session.query(Task).filter(Task.user_id == user.id).count()
            print(f"  • {user.name} (@{user.username}) - {tasks} tarefas")

        print("\nTarefas:")
        tasks = session.query(Task).limit(5).all()
        for task in tasks:
            print(f"  • {task.title} ({task.status}) - @{task.user.username}")

    except Exception as e:
        print(f"Erro ao mostrar dados: {e}")


if __name__ == "__main__":
    print("MIGRATION - Criando dados de exemplo")
    print("=" * 40)

    create_sample_data()

    print("\nPronto! Execute a API:")
    print("uvicorn src.main:app --host 0.0.0.0 --port 8001")
