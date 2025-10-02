/*-------------Totem do usuario-------------*/
async function takeTicket(category){
  try {
    const res = await fetch(`${API_URL_NODE}/nova_senha`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({category})
    });

    if(!res.ok){
      const errorData = await res.json().catch(() => ({error: 'Erro desconhecido'}));
      alert(`Ocorreu um erro no servidor: ${errorData.error || 'Código de status: ' + res.status}`);
      console.error("Erro na requisição de geração de senha!", res.status, errorData);
      return;
    }

    const data = await res.json();

    // Impressora está offline antes de gerar senha
    if(data.status === "erro_impressao" && !data.senha){
      console.warn("Impressora offline, senha não gerada!");
      showCustomAlert(`🚨 A impressora está offline!\nPor favor, aguarde o suporte.`, 8000);
      return;
    }

    // Impressão OK
    if(data.status === "impresso" && data.senha){
      console.log("Senha gerada e impressa:", data.senha);
      showCustomAlert(`Sua senha é ${data.senha}. Aguarde ser chamado!`, 5000);
      return;
    }

    // Impressora falhou depois de gerar a senha
    if(data.status === "erro_impressao" && data.senha){
      console.warn("Falha na impressão. Exibindo senha na tela:", data.senha);
      showCustomAlert(`⚠️ Impressora falhou!\nAnote sua senha:\n\nSENHA: ${data.senha}`, 8000);
      return;
    }

    // Caso inesperado
    console.log("Resposta inesperada:", data);
    showCustomAlert(`Não foi possível gerar a senha. Tente novamente.`, 5000);

  } catch (err) {
    console.error("Erro na comunicação com o servidor: ", err);
    showCustomAlert(`❌ Falha de comunicação com o servidor.`, 5000);
  }
}

// Alerta customizado
function showCustomAlert(message, duration = 5000) {
    const alertBox = document.getElementById("alert-box");
    const overlay = document.getElementById("overlay"); // Referência ao novo elemento

    // 1. MOSTRAR: Exibe a caixa de alerta E a camada de bloqueio
    alertBox.innerText = message;
    alertBox.style.display = "block";
    overlay.style.display = "block"; 

    // 2. ESCONDER: Agenda o desaparecimento dos dois elementos
    setTimeout(() => {
        alertBox.style.display = "none";
        overlay.style.display = "none";
    }, duration);
}
/*-------------Totem do usuario-------------*/
