// ==================================================
// ESTADO
// ==================================================

let turmaAtual = null;   // detalhe da turma aberta no momento
let alunoHistoricoAtual = null;

// ==================================================
// UTIL
// ==================================================

function formatarDataBR(dataIso) {

  if (!dataIso) return "—";

  const [ano, mes, dia] = dataIso.split("-");

  return `${dia}/${mes}/${ano}`;
}

function mostrarToast(mensagem, tipo = "sucesso") {

  const toast = document.getElementById("toast");

  toast.textContent = mensagem;
  toast.className = `toast visivel ${tipo}`;

  setTimeout(() => {
    toast.classList.remove("visivel");
  }, 3500);
}

async function chamarApi(url, opcoes = {}) {

  const resposta = await fetch(url, opcoes);

  const corpo = await resposta.json().catch(() => ({}));

  if (!resposta.ok) {

    if (resposta.status === 403) {
      throw new Error("Você não tem acesso a este recurso.");
    }

    throw new Error(corpo.erro || "Não foi possível concluir a ação. Tente novamente.");
  }

  return corpo;
}

function abrirModal(id) {
  document.getElementById(id).classList.remove("oculto");
}

function fecharModal(id) {
  document.getElementById(id).classList.add("oculto");
}

document.querySelectorAll(".modal-fechar").forEach((botao) => {
  botao.addEventListener("click", () => fecharModal(botao.dataset.fechar));
});

// ==================================================
// DASHBOARD
// ==================================================

async function carregarDashboard() {

  try {

    const dados = await chamarApi("/api/professor/dashboard");

    document.getElementById("saudacao").textContent = `Bem-vindo(a), ${dados.nome}`;
    document.getElementById("resumo-turmas").textContent = dados.quantidade_turmas;
    document.getElementById("resumo-disciplinas").textContent = dados.quantidade_disciplinas;
    document.getElementById("resumo-cursos").textContent = dados.quantidade_cursos;
    document.getElementById("resumo-alunos").textContent = dados.total_alunos;

  } catch (erro) {
    mostrarToast(erro.message, "erro");
  }
}

// ==================================================
// MINHAS TURMAS
// ==================================================

async function carregarTurmas() {

  const status = document.getElementById("status-turmas");
  const grade = document.getElementById("grade-turmas");

  status.classList.remove("erro");
  status.textContent = "Carregando turmas...";
  grade.innerHTML = "";

  try {

    const turmas = await chamarApi("/api/professor/turmas");

    if (!turmas.length) {

      status.textContent = "";

      grade.innerHTML = `
        <div class="vazio">
          Você ainda não possui turmas vinculadas.
        </div>
      `;

      return;
    }

    status.textContent = `${turmas.length} turma(s).`;

    for (const turma of turmas) {

      const card = document.createElement("div");

      card.className = "card turma-card";

      card.innerHTML = `
        <h3>${turma.nome_turma}</h3>
        <p class="subinfo">${turma.curso} · ${turma.disciplina}</p>
        <span class="turma-alunos">${turma.quantidade_alunos} aluno(s)</span>
        <button class="botao-primario" type="button">Abrir Turma</button>
      `;

      card.querySelector("button").addEventListener(
        "click",
        () => abrirTurma(turma.id_turma)
      );

      grade.appendChild(card);
    }

  } catch (erro) {

    status.textContent = erro.message;
    status.classList.add("erro");
  }
}

// ==================================================
// DETALHE DA TURMA
// ==================================================

function badgeSituacao(situacao) {

  const mapa = {
    "Ativa": "badge-ativa",
    "Trancada": "badge-trancada",
  };

  const classe = mapa[situacao] || "badge-inativa";

  return `<span class="badge ${classe}">${situacao}</span>`;
}

function formatarFrequencia(frequencia) {

  if (frequencia === null || frequencia === undefined) {
    return '<span class="subinfo">Sem registros</span>';
  }

  const classe = frequencia >= 75 ? "freq-boa" : "freq-baixa";

  return `<span class="${classe}">${frequencia}%</span>`;
}

async function abrirTurma(idTurma) {

  document.getElementById("secao-dashboard").classList.add("oculto");
  document.getElementById("secao-turmas").classList.add("oculto");
  document.getElementById("secao-detalhe-turma").classList.remove("oculto");

  const status = document.getElementById("status-detalhe");
  const corpo = document.getElementById("corpo-alunos");

  status.classList.remove("erro");
  status.textContent = "Carregando turma...";
  corpo.innerHTML = "";

  try {

    const turma = await chamarApi(`/api/professor/turmas/${idTurma}`);

    turmaAtual = turma;

    document.getElementById("detalhe-nome-turma").textContent = turma.nome_turma;
    document.getElementById("detalhe-info-turma").textContent =
      `${turma.curso} · ${turma.disciplina} · ${turma.turno || "—"} · ${turma.ano_letivo || "—"}`;

    if (!turma.alunos.length) {

      status.textContent = "";

      corpo.innerHTML = `
        <tr><td colspan="5" class="vazio">Nenhum aluno matriculado nesta turma.</td></tr>
      `;

      return;
    }

    status.textContent = `${turma.alunos.length} aluno(s).`;

    for (const aluno of turma.alunos) {

      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${aluno.nome}</td>
        <td>${badgeSituacao(aluno.situacao)}</td>
        <td>${aluno.media_atual ?? '<span class="subinfo">Sem notas</span>'}</td>
        <td>${formatarFrequencia(aluno.frequencia)}</td>
        <td>
          <button class="botao-pequeno" data-acao="nota">Nota</button>
          <button class="botao-pequeno" data-acao="historico">Histórico</button>
        </td>
      `;

      tr.querySelector('[data-acao="nota"]').addEventListener(
        "click",
        () => abrirModalNota(aluno.id_aluno, aluno.nome)
      );

      tr.querySelector('[data-acao="historico"]').addEventListener(
        "click",
        () => abrirHistorico(aluno.id_aluno, aluno.nome)
      );

      corpo.appendChild(tr);
    }

  } catch (erro) {

    status.textContent = erro.message;
    status.classList.add("erro");
  }
}

function voltarParaTurmas() {

  turmaAtual = null;

  document.getElementById("secao-detalhe-turma").classList.add("oculto");
  document.getElementById("secao-dashboard").classList.remove("oculto");
  document.getElementById("secao-turmas").classList.remove("oculto");

  carregarTurmas();
  carregarDashboard();
}

// ==================================================
// MODAL: NOTA
// ==================================================

let alunoNotaAtual = null;

function abrirModalNota(idAluno, nomeAluno) {

  alunoNotaAtual = idAluno;

  document.getElementById("nota-nome-aluno").textContent = nomeAluno;
  document.getElementById("form-nota").reset();

  const mensagem = document.getElementById("mensagem-nota");
  mensagem.textContent = "";
  mensagem.className = "mensagem";

  abrirModal("modal-nota");
}

async function enviarNota(evento) {

  evento.preventDefault();

  const mensagem = document.getElementById("mensagem-nota");

  const dados = {
    id_turma: turmaAtual.id_turma,
    id_aluno: alunoNotaAtual,
    tipo_avaliacao: document.getElementById("nota-avaliacao").value.trim(),
    nota: document.getElementById("nota-valor").value,
    observacoes: document.getElementById("nota-observacoes").value.trim() || null,
  };

  try {

    await chamarApi("/api/professor/notas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    mensagem.textContent = "Nota lançada com sucesso.";
    mensagem.className = "mensagem sucesso";

    mostrarToast("Nota lançada com sucesso.", "sucesso");

    setTimeout(() => fecharModal("modal-nota"), 700);

    abrirTurma(turmaAtual.id_turma);

  } catch (erro) {

    mensagem.textContent = erro.message;
    mensagem.className = "mensagem erro";
  }
}

// ==================================================
// MODAL: PRESENÇA DA TURMA
// ==================================================

function abrirModalPresenca() {

  if (!turmaAtual || !turmaAtual.alunos.length) {
    mostrarToast("Não há alunos nesta turma para registrar presença.", "erro");
    return;
  }

  document.getElementById("form-presenca").reset();

  const lista = document.getElementById("lista-presenca-alunos");
  lista.innerHTML = "";

  for (const aluno of turmaAtual.alunos) {

    const linha = document.createElement("div");

    linha.className = "linha-presenca";

    linha.innerHTML = `
      <span>${aluno.nome}</span>
      <select data-id-aluno="${aluno.id_aluno}">
        <option value="P" selected>Presente</option>
        <option value="F">Ausente</option>
        <option value="A">Atestado</option>
        <option value="J">Justificado</option>
      </select>
    `;

    lista.appendChild(linha);
  }

  const mensagem = document.getElementById("mensagem-presenca");
  mensagem.textContent = "";
  mensagem.className = "mensagem";

  abrirModal("modal-presenca");
}

async function enviarPresenca(evento) {

  evento.preventDefault();

  const mensagem = document.getElementById("mensagem-presenca");

  const selects = document.querySelectorAll("#lista-presenca-alunos select");

  const presencas = [...selects].map((select) => ({
    id_aluno: parseInt(select.dataset.idAluno, 10),
    situacao: select.value,
  }));

  const dados = {
    id_turma: turmaAtual.id_turma,
    data_aula: document.getElementById("presenca-data").value,
    periodo: document.getElementById("presenca-periodo").value,
    presencas,
  };

  try {

    await chamarApi("/api/professor/presencas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    mensagem.textContent = "Presença registrada com sucesso.";
    mensagem.className = "mensagem sucesso";

    mostrarToast("Presença registrada com sucesso.", "sucesso");

    setTimeout(() => fecharModal("modal-presenca"), 700);

    abrirTurma(turmaAtual.id_turma);

  } catch (erro) {

    mensagem.textContent = erro.message;
    mensagem.className = "mensagem erro";
  }
}

// ==================================================
// MODAL: HISTÓRICO
// ==================================================

async function abrirHistorico(idAluno, nomeAluno) {

  alunoHistoricoAtual = idAluno;

  document.getElementById("historico-nome-aluno").textContent = nomeAluno;

  abrirModal("modal-historico");

  trocarAbaHistorico("notas");

  try {

    const [notas, presencas] = await Promise.all([
      chamarApi(`/api/professor/turmas/${turmaAtual.id_turma}/alunos/${idAluno}/notas`),
      chamarApi(`/api/professor/turmas/${turmaAtual.id_turma}/alunos/${idAluno}/presencas`),
    ]);

    document.getElementById("historico-media").textContent =
      notas.media !== null && notas.media !== undefined ? notas.media : "Sem notas";

    const corpoNotas = document.getElementById("corpo-historico-notas");

    corpoNotas.innerHTML = notas.notas.length
      ? notas.notas.map((n) => `
          <tr>
            <td>${n.tipo_avaliacao}</td>
            <td>${n.nota}</td>
            <td>${n.observacoes || "—"}</td>
          </tr>
        `).join("")
      : `<tr><td colspan="3" class="vazio">Nenhuma nota lançada ainda.</td></tr>`;

    document.getElementById("historico-frequencia").textContent =
      presencas.percentual_frequencia !== null && presencas.percentual_frequencia !== undefined
        ? `${presencas.percentual_frequencia}%`
        : "—";

    document.getElementById("historico-total-presencas").textContent = presencas.total_presencas;
    document.getElementById("historico-total-faltas").textContent = presencas.total_faltas;

    const corpoPresencas = document.getElementById("corpo-historico-presencas");

    corpoPresencas.innerHTML = presencas.registros.length
      ? presencas.registros.map((p) => `
          <tr>
            <td>${formatarDataBR(p.data_aula)}</td>
            <td>${p.periodo || "—"}</td>
            <td>${p.status}</td>
          </tr>
        `).join("")
      : `<tr><td colspan="3" class="vazio">Nenhuma presença registrada ainda.</td></tr>`;

  } catch (erro) {
    mostrarToast(erro.message, "erro");
  }
}

function trocarAbaHistorico(aba) {

  document.querySelectorAll(".aba-historico").forEach((botao) => {
    botao.classList.toggle("ativa", botao.dataset.aba === aba);
  });

  document.getElementById("historico-notas").classList.toggle("oculto", aba !== "notas");
  document.getElementById("historico-presencas").classList.toggle("oculto", aba !== "presencas");
}

document.querySelectorAll(".aba-historico").forEach((botao) => {
  botao.addEventListener("click", () => trocarAbaHistorico(botao.dataset.aba));
});

// ==================================================
// EVENTOS
// ==================================================

document.getElementById("botao-recarregar-turmas").addEventListener("click", carregarTurmas);
document.getElementById("botao-voltar").addEventListener("click", voltarParaTurmas);
document.getElementById("botao-abrir-presenca").addEventListener("click", abrirModalPresenca);
document.getElementById("form-nota").addEventListener("submit", enviarNota);
document.getElementById("form-presenca").addEventListener("submit", enviarPresenca);

// ==================================================
// INICIALIZAÇÃO
// ==================================================

carregarDashboard();
carregarTurmas();