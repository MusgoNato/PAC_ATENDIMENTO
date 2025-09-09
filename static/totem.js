
/*-------------Totem do usuario-------------*/
async function takeTicket(category){
      try {
        const res = await fetch(`${API_URL_NODE}/nova_senha`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({category})
        });

        if(!res.ok){
          alert('Sistema não está respondendo, aguarde um momento');
          console.error("Erro na requisição de geração de senha!");
          return;
        }

        const data = await res.json();
        console.log(`Data: ${data.senha}`);
        if (data.senha){
          console.log("Senha gerada: ", data.senha);
          alert(`Sua senha é ${data.senha}, aguarde ser chamado!`);
        }else{
          alert('Erro ao processar a senha. Por favor, tente novamente.');
        }

      }catch (err)
      {
        console.error("Erro na comunicação com o servidor: ", err);
        alert("O sistema está offline. Por favor, tente novamente mais tarde!");
      }
}
/*-------------Totem do usuario-------------*/