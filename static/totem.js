/*-------------Totem do usuario-------------*/
async function takeTicket(category) {
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
/*-------------Totem do usuario-------------*/
