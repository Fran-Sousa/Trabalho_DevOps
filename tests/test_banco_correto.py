#!/usr/bin/env python3
"""
Teste simples do banco de dados
Versão simplificada - apenas o essencial!
"""

import sys
import os

# Adiciona o diretório src ao path para os imports funcionarem
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.db import session, User, Task

def testar_banco():
    """Testa o banco de forma simples."""
    try:
        # Testa conexão
        user_count = session.query(User).count()
        task_count = session.query(Task).count()
        
        print("✅ BANCO OK")
        print(f"   👥 {user_count} usuários")
        print(f"   📋 {task_count} tarefas")
        
        return True
        
    except Exception as e:
        print(f"❌ BANCO ERRO: {e}")
        return False

def testar_consultas():
    """Testa consultas de forma simples."""
    try:
        # Consultas básicas
        todo_count = session.query(Task).filter(Task.status == 'todo').count()
        done_count = session.query(Task).filter(Task.status == 'done').count()
        urgent_count = session.query(Task).filter(Task.priority == 'urgent').count()
        
        print("✅ CONSULTAS OK")
        print(f"   📝 {todo_count} tarefas a fazer")
        print(f"   ✅ {done_count} tarefas concluídas")
        print(f"   🚨 {urgent_count} tarefas urgentes")
        
        return True
        
    except Exception as e:
        print(f"❌ CONSULTAS ERRO: {e}")
        return False

def main():
    """Teste principal - simples e direto."""
    print("🚀 TESTE RÁPIDO DO BANCO")
    print("=" * 30)
    
    # Testa banco
    banco_ok = testar_banco()
    
    # Testa consultas
    consultas_ok = testar_consultas()
    
    # Resultado final
    print("\n" + "=" * 30)
    if banco_ok and consultas_ok:
        print("🎉 TUDO FUNCIONANDO!")
    else:
        print("⚠️  ALGUNS PROBLEMAS DETECTADOS")
    
    print("=" * 30)

if __name__ == "__main__":
    main()
