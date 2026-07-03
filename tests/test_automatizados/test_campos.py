def test_cadastro_sem_nome(client):
    response = client.post(
        "/cadastro",
        data={
            "nome": "Pietro",
            "email": "teste@email.com",
            "senha": "123456",
            "confirmar_senha": "123456",
            "tipo": "aluno"
        },
        follow_redirects=True
    )

    assert b"Preencha todos os campos" in response.data
    
    
def test_cadastro_sem_confirmar_senha(client):
    response = client.post(
        "/cadastro",
            data={
            "nome": "Pietro",
            "email": "teste@email.com",
            "senha": "123456",
            "confirmar_senha": "",
            "tipo": "aluno"
        },
        follow_redirects=True
    )

    assert b"As senhas n\xc3\xa3o conferem" in response.data