#!/usr/bin/env python3
"""
Script simples para adicionar dados ao banco
Uso rápido para adicionar usuários e tarefas!
"""

import os
import sys

# Adiciona o diretório src ao path para os imports funcionarem
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from database.db import Task, User, session


def adicionar_usuario_rapido(nome, username, senha):
    """Adiciona um usuário de forma rápida."""
    try:
        # Verifica se já existe
        if session.query(User).filter(User.username == username).first():
            print(f"⚠️  Usuário @{username} já existe!")
            return False

        # Cria usuário
        novo_usuario = User(name=nome, username=username, password=senha)
        session.add(novo_usuario)
        session.commit()

        print(f"✅ Usuário {nome} (@{username}) criado! ID: {novo_usuario.id}")
        return True

    except Exception as e:
        print(f"❌ Erro: {e}")
        session.rollback()
        return False


def adicionar_tarefa_rapida(titulo, status, prioridade, username_responsavel):
    """Adiciona uma tarefa de forma rápida."""
    try:
        # Busca usuário pelo username
        usuario = (
            session.query(User)
            .filter(User.username == username_responsavel)
            .first()
        )
        if not usuario:
            print(f"❌ Usuário @{username_responsavel} não encontrado!")
            return False

        # Cria tarefa
        nova_tarefa = Task(
            title=titulo, status=status, priority=prioridade, user_id=usuario.id
        )

        session.add(nova_tarefa)
        session.commit()

        print(f"✅ Tarefa '{titulo}' criada! Responsável: {usuario.name}")
        return True

    except Exception as e:
        print(f"❌ Erro: {e}")
        session.rollback()
        return False


def main():
    """Exemplos de uso rápido."""
    print("🚀 ADICIONANDO DADOS AO BANCO")
    print("=" * 40)

    try:
        # Testa conexão
        user_count = session.query(User).count()
        print(f"✅ Conectado! {user_count} usuários encontrados\n")

        #  Adicionar usuário
        print("👤 EXEMPLO: Adicionando usuário...")
        # Adicionar dados 'nome' 'user' 'senha'
        adicionar_usuario_rapido("Igor", "Igor", "123456")

        # Adicionar tarefa
        print("\n📋 EXEMPLO: Adicionando tarefa...")
        # Criar tarefa 'Titulo', 'Status', 'Dificuldade', 'User'
        adicionar_tarefa_rapida("TESTE", "todo", "Alta", "Igor")

        # print("\n📋 EXEMPLO: Adicionando outra tarefa...")
        # adicionar_tarefa_rapida(
        #     "Revisar interface", "in_progress", "high", "admin"
        # )

        print("\n🎉 Exemplos executados!")
        print("\n💡 DICA: Use as funções diretamente no seu código!")

    except Exception as e:
        print(f"❌ Erro de conexão: {e}")


if __name__ == "__main__":
    main()
