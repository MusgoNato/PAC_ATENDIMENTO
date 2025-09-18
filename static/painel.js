const socket = io(URL_WEBSOCKET);

// Atualiza o relógio em tempo real
function atualizarRelogio() {
  const agora = new Date();
  const hora = String(agora.getHours()).padStart(2, '0');
  const min = String(agora.getMinutes()).padStart(2, '0');
  const seg = String(agora.getSeconds()).padStart(2, '0');
  const texto = `${hora}:${min}:${seg}`;
  document.getElementById("relogioNormal").textContent = texto;
  document.getElementById("relogioChamada").textContent = texto;
}
setInterval(atualizarRelogio, 1000);
atualizarRelogio();

// Função para alternar os painéis
function chamarSenha(senha, guiche) {
  document.getElementById("senhaChamada").textContent = senha;
  document.getElementById("guicheChamada").textContent = guiche;

  // toca o som
  document.getElementById("somChamada").play();

  // mostra painel de chamada
  document.getElementById("painelNormal").classList.remove("ativo");
  document.getElementById("painelChamada").classList.add("ativo");

  // volta pro normal depois de 7s
  setTimeout(() => {
    document.getElementById("painelChamada").classList.remove("ativo");
    document.getElementById("painelNormal").classList.add("ativo");
  }, 7000);
}

// Quando a fila é atualizada
socket.on("fila_atualizada", async () => {
  try {
    const response = await fetch(`${API_URL_NODE}/api/painel`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    const data = await response.json();

    if (!data.success) return;

    // Atualiza a fila na tela
    const filaDiv = document.querySelector("#painelNormal .fila");
    filaDiv.innerHTML = "<p>Fila</p>";
    data.fila.forEach(item => {
      filaDiv.innerHTML += `<p>${item.senha}</p>`;
    });

    // Atualiza guichês
    const guichesDiv = document.querySelector("#painelNormal .guiches");
    guichesDiv.innerHTML = "";
    data.guiches.forEach(g => {
      guichesDiv.innerHTML += `<div class="guiche">Guichê ${g.numero}<br>${g.senha}</div>`;
    });

    // Se tiver senha chamada, mostra em destaque
    if (data.senha_chamada) {
      chamarSenha(data.senha_chamada, data.guiche);
    }

  } catch (err) {
    console.error("Erro ao buscar dados do painel:", err);
  }
});
function atualizarData() {
  const agora = new Date();
  const dias = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"];
  const meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  const diaSemana = dias[agora.getDay()];
  const dia = String(agora.getDate()).padStart(2, '0');
  const mes = meses[agora.getMonth()];
  const ano = agora.getFullYear();
  const texto = `${diaSemana}, ${dia} de ${mes} de ${ano}`;
  document.getElementById("dataAtual").textContent = texto;
}
atualizarData();
