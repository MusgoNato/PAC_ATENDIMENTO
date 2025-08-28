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


document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('animar-btn');
  const topo = document.getElementById('painel-topo-texto');
  const guiche1 = document.getElementById('guiche1-conteudo');
  if (btn && topo-texto && guiche1) {
    btn.addEventListener('click', function() {
      // Fade out topo-texto
      topo.classList.add('fade-out');
      setTimeout(() => {
        topo.style.visibility = 'hidden';
        // Fade in no guiche
        guiche1.textContent = topo-texto.textContent;
        guiche1.classList.add('fade-in');
        setTimeout(() => {
          guiche1.classList.remove('fade-in');
        }, 700);
      }, 700);
    });
  }
});