
/*-------------Totem do usuario-------------*/
async function takeTicket(category){
      try {
        const res = await fetch('/totem/nova_senha', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "category": category})
        });

        if(!res.ok){
          alert('Sistema não está respondendo, aguarde um momento');
          return;
        }

        const data = await res.json();
        console.log("Senha gerada: ", data.senha);

      }catch (err)
      {
        console.error("Erro: ", err);
      }
}
/*-------------Totem do usuario-------------*/