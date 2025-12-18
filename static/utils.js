/* Exportação de funções personalizadas */
export function confirmPersonalizado(mensagem) {
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

export function alertPersonalizado(mensagem) {
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
