/*-------------Totem do usuario-------------*/
async function takeTicket(category) {
    console.log(`CAtegoy enviado ao take ticket : ${category}`);
    try {
        const res = await fetch(`${API_URL_NODE}/nova_senha`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category })
        });

        // =======================================================
        // TRATAMENTO DE ERROS HTTP (Status != 200)
        // =======================================================
        if (!res.ok) {
            // O Node.js enviará a mensagem de erro no corpo JSON
            const errorData = await res.json().catch(() => ({ message: 'Erro desconhecido' }));
            
            // 503 SERVICE UNAVAILABLE (Impressora Offline)
            if (res.status === 503) {
                console.warn("Impressora offline, senha não gerada (Erro 503).");
                showCustomAlert(`🚨 A impressora está offline!\nPor favor, aguarde o suporte.`, 8000);
                return;
            }

            // 500 INTERNAL SERVER ERROR (Falha crítica no Flask/DB)
            if (res.status === 500) {
                console.error("Erro crítico na requisição de geração de senha!", res.status, errorData);
                alert(`Ocorreu um erro no servidor: ${errorData.message || 'Código de status: ' + res.status}`);
                return;
            }

            // Outros erros
            alert(`Ocorreu um erro inesperado: ${errorData.message || 'Código de status: ' + res.status}`);
            console.error("Erro inesperado na requisição:", res.status, errorData);
            return;
        }

        // =======================================================
        // TRATAMENTO DE SUCESSO (Status 200 OK)
        // =======================================================
        
        const data = await res.json();
        const ticketNumber = data.ticket_number; // Usa o número retornado pelo Flask
        console.log(data);

        // TODO (ESTA RETORNANDO UMA MENSAGEM, DEVERIA RETORNAR O NUMERO DO TICKET)

        // 200 OK significa que:
        // 1. A impressora estava online.
        // 2. O ticket foi criado no Flask.
        // 3. O ZPL foi enviado para o Raspberry Pi.
        
        console.log("Senha gerada e enviada para impressão:", ticketNumber);
        
        // Mensagem de sucesso simples
        showCustomAlert(`Sua senha é ${ticketNumber}.\nAguarde ser chamado!`, 5000);

    } catch (err) {
        // Falha de rede (ex: servidor Node.js totalmente inacessível)
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


/**
 * TODO:
 *  
 * Veja que esta função esta duplicada, é identica a função utilizada no script atendente.js. Portanto, a tarefa é encontrar uma forma de chamar a
 * mesma função com nome 'confirmPersonalizado' para ambos arquivos (atendente.js e totem.js). 
 * Aqui vai uma dica, procure sobre modularização de código.  
 * 
 */
function confirmPersonalizadoTotem(mensagem) {
    return new Promise((resolve) => {

        // Cria o overlay
        const overlay = document.createElement("div");
        overlay.style = `
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.45);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 99999;
        `;

        // Cria o modal
        const box = document.createElement("div");
        box.style = `
            background: white;
            padding: 20px;
            border-radius: 10px;
            width: 320px;
            text-align: center;
            font-family: Arial;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        `;

        box.innerHTML = `
            <p style="font-size: 18px; margin-bottom: 20px;">${mensagem}</p>
            <button id="btnConfirmSim" style="padding: 10px 20px; margin-right: 10px;">Sim</button>
            <button id="btnConfirmNao" style="padding: 10px 20px;">Não</button>
        `;

        overlay.appendChild(box);
        document.body.appendChild(overlay);

        // Eventos
        document.getElementById("btnConfirmSim").onclick = () => {
            overlay.remove();
            resolve(true);
        };

        document.getElementById("btnConfirmNao").onclick = () => {
            overlay.remove();
            resolve(false);
        };
    });
}

function alertPersonalizadoTotem(mensagem) {
    return new Promise((resolve) => {

        // Criar overlay
        const overlay = document.createElement("div");
        overlay.style = `
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.45);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 99999;
        `;

        // Criar caixa
        const box = document.createElement("div");
        box.style = `
            background: white;
            padding: 20px;
            border-radius: 10px;
            width: 320px;
            text-align: center;
            font-family: Arial;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        `;

        box.innerHTML = `
            <p style="font-size: 18px; margin-bottom: 20px;">${mensagem}</p>
            <button id="alertOkBtn" style="padding: 10px 25px; font-size: 15px;">OK</button>
        `;

        overlay.appendChild(box);
        document.body.appendChild(overlay);

        // Botão OK
        document.getElementById("alertOkBtn").onclick = () => {
            overlay.remove();
            resolve(); // Não retorna nada, igual o alert nativo
        };
    });
}
/*-------------Totem do usuario-------------*/
