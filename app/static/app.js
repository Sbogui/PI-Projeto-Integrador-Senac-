const COLUNAS = {

  professores: [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
    { chave: "email", titulo: "E-mail" },
    { chave: "disciplina", titulo: "Disciplina" },
  ],


  alunos: [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
    { chave: "email", titulo: "E-mail" },
    { chave: "telefone", titulo: "Telefone" },
    { chave: "curso_id", titulo: "Curso" },
  ],

  cursos: [
    { chave: "id_curso", titulo: "ID" },
    { chave: "nome_curso", titulo: "Curso" },
    { chave: "carga_horaria", titulo: "Carga Horária" },
    { chave: "disciplinas", titulo: "Disciplinas" }
  ],

  disciplinas: [
    { chave: "id_disciplina", titulo: "ID" },
    { chave: "nome_disciplina", titulo: "Disciplina" },
    { chave: "carga_horaria", titulo: "Carga Horária" },
    { chave: "id_curso", titulo: "Curso" },
    { chave: "id_professor", titulo: "Professor" }
  ],

  matriculas: [
    { chave: "id_matricula", titulo: "ID" },
    { chave: "data_matricula", titulo: "Data" },
    { chave: "situacao", titulo: "Situação" },
    { chave: "id_aluno", titulo: "Aluno" },
    { chave: "id_curso", titulo: "Curso" },
  ],

  notas: [
    { chave: "id_nota", titulo: "ID" },
    { chave: "nota", titulo: "Nota" },
    { chave: "tipo_avaliacao", titulo: "Avaliação" },
    { chave: "id_aluno", titulo: "Aluno" },
    { chave: "id_disciplina", titulo: "Disciplina" },
  ],

  presencas: [
    { chave: "id_presenca", titulo: "ID" },
    { chave: "data_aula", titulo: "Data" },
    { chave: "presente", titulo: "Presente" },
    { chave: "id_aluno", titulo: "Aluno" },
    { chave: "id_disciplina", titulo: "Disciplina" },
  ],

  telefones: [
    { chave: "id_telefone", titulo: "ID" },
    { chave: "numero_pessoal", titulo: "Pessoal" },
    { chave: "numero_profissional", titulo: "Profissional" },
  ],

  emails: [
    { chave: "id_email", titulo: "ID" },
    { chave: "email_pessoal", titulo: "Pessoal" },
    { chave: "email_profissional", titulo: "Profissional" },
  ],

  enderecos: [
    { chave: "id_endereco", titulo: "ID" },
    { chave: "rua", titulo: "Rua" },
    { chave: "cidade", titulo: "Cidade" },
    { chave: "estado", titulo: "Estado" },
  ],

};

const TITULOS = {

  professores: {
    lista: "Professores",
    form: "Novo professor"
  },


  alunos: {
    lista: "Alunos",
    form: "Novo aluno"
  },

  cursos: {
    lista: "Cursos",
    form: "Novo curso"
  },

  disciplinas: {
    lista: "Disciplinas",
    form: "Nova disciplina"
  },

  matriculas: {
    lista: "Matrículas",
    form: "Nova matrícula"
  },

  notas: {
    lista: "Notas",
    form: "Nova nota"
  },

  presencas: {
    lista: "Presenças",
    form: "Nova presença"
  },

  telefones: {
    lista: "Telefones",
    form: "Novo telefone"
  },

  emails: {
    lista: "Emails",
    form: "Novo email"
  },

  enderecos: {
    lista: "Endereços",
    form: "Novo endereço"
  },

};

const CAMPOS = {

  professores: [
    { nome: "nome", rotulo: "Nome", obrigatorio: true },
    { nome: "email", rotulo: "E-mail", tipo: "email" },
    { nome: "disciplina", rotulo: "Disciplina" },
  ],


  alunos: [
    { nome: "nome", rotulo: "Nome", obrigatorio: true },
    { nome: "email", rotulo: "E-mail", tipo: "email" },
    { nome: "telefone", rotulo: "Telefone" },

    {
      nome: "curso_id", rotulo: "Curso", tipo: "select", origem: "cursos", obrigatorio: true
    },
  ],

  cursos: [
    { nome: "nome_curso", rotulo: "Curso", obrigatorio: true },
    { nome: "carga_horaria", rotulo: "Carga Horária" },

    {
      nome: "id_professor",
      rotulo: "Professor",
      tipo: "select",
      origem: "professores",
      obrigatorio: true
    },
  ],

  disciplinas: [
    {
      nome: "nome_disciplina",
      rotulo: "Disciplina",
      obrigatorio: true
    },

    {
      nome: "carga_horaria",
      rotulo: "Carga Horária"
    },

    {
      nome: "id_curso",
      rotulo: "Curso",
      tipo: "select",
      origem: "cursos",
      obrigatorio: true
    },

    {
    nome: "id_professor",
    rotulo: "Professor",
    tipo: "select",
    origem: "professores",
    obrigatorio: true
    },
  ],

  matriculas: [
    {
      nome: "data_matricula",
      rotulo: "Data Matrícula",
      obrigatorio: true
    },

    {
      nome: "situacao",
      rotulo: "Situação",
      obrigatorio: true
    },

    {
      nome: "id_aluno",
      rotulo: "Aluno",
      tipo: "select",
      origem: "alunos",
      obrigatorio: true
    },

    {
      nome: "id_curso",
      rotulo: "Curso",
      tipo: "select",
      origem: "cursos",
      obrigatorio: true
    },
  ],

  notas: [
    {
      nome: "nota",
      rotulo: "Nota",
      obrigatorio: true
    },

    {
      nome: "tipo_avaliacao",
      rotulo: "Avaliação",
      obrigatorio: true
    },

    {
      nome: "id_aluno",
      rotulo: "Aluno",
      tipo: "select",
      origem: "alunos",
      obrigatorio: true
    },

    {
      nome: "id_disciplina",
      rotulo: "Disciplina",
      tipo: "select",
      origem: "disciplinas",
      obrigatorio: true
    },
  ],

  presencas: [
    {
      nome: "data_aula",
      rotulo: "Data Aula",
      obrigatorio: true
    },

    {
      nome: "presente",
      rotulo: "Presente",
      obrigatorio: true
    },

    {
      nome: "id_aluno",
      rotulo: "Aluno",
      tipo: "select",
      origem: "alunos",
      obrigatorio: true
    },

    {
      nome: "id_disciplina",
      rotulo: "Disciplina",
      tipo: "select",
      origem: "disciplinas",
      obrigatorio: true
    },
  ],

  telefones: [
    {
      nome: "numero_pessoal",
      rotulo: "Telefone Pessoal"
    },

    {
      nome: "numero_profissional",
      rotulo: "Telefone Profissional"
    },
  ],

  emails: [
    {
      nome: "email_pessoal",
      rotulo: "Email Pessoal"
    },

    {
      nome: "email_profissional",
      rotulo: "Email Profissional"
    },
  ],

  enderecos: [
    {
      nome: "rua",
      rotulo: "Rua"
    },

    {
      nome: "cidade",
      rotulo: "Cidade"
    },

    {
      nome: "estado",
      rotulo: "Estado"
    },
  ],

};

const elementoStatus = document.getElementById("status");
const elementoTituloLista = document.getElementById("titulo-lista");
const elementoTituloFormulario = document.getElementById("titulo-formulario");
const elementoCabecalho = document.getElementById("cabecalho");
const elementoCorpo = document.getElementById("corpo");
const elementoCampos = document.getElementById("campos");
const formulario = document.getElementById("formulario");
const mensagemFormulario = document.getElementById("mensagem-formulario");
const botaoRecarregar = document.getElementById("botao-recarregar");
const abas = document.querySelectorAll(".aba");


let tipoAtual = "professores";
let idEditando = null;

async function buscar(tipo) {
  const resposta = await fetch(`/api/${tipo}`);

  if (!resposta.ok) {
    throw new Error(`HTTP ${resposta.status}`);
  }

  return resposta.json();
}

async function carregar(tipo) {

  tipoAtual = tipo;

  elementoTituloLista.textContent =
    TITULOS[tipo].lista;

  elementoTituloFormulario.textContent =
    TITULOS[tipo].form;

  limparMensagem();

  await renderizarFormulario(tipo);

  renderizarCabecalho(tipo);

  elementoCorpo.innerHTML = "";

  elementoStatus.classList.remove("erro");

  elementoStatus.textContent = "Carregando...";

  try {

    const dados = await buscar(tipo);

    renderizarLinhas(tipo, dados);

    elementoStatus.textContent =
      `${dados.length} registro(s) carregado(s).`;

  } catch (erro) {

    elementoStatus.textContent =
      `Falha ao carregar: ${erro.message}`;

    elementoStatus.classList.add("erro");
  }
}

function renderizarCabecalho(tipo) {

  elementoCabecalho.innerHTML = "";

  for (const coluna of COLUNAS[tipo]) {

    const th = document.createElement("th");

    th.textContent = coluna.titulo;

    elementoCabecalho.appendChild(th);
  }

  const thAcoes = document.createElement("th");

  thAcoes.textContent = "Ações";

  elementoCabecalho.appendChild(thAcoes);
}

function renderizarLinhas(tipo, dados) {

  elementoCorpo.innerHTML = "";

  if (!dados.length) {

    const tr = document.createElement("tr");

    const td = document.createElement("td");

    td.colSpan = COLUNAS[tipo].length + 1;

    td.className = "vazio";

    td.textContent = "Nenhum registro encontrado.";

    tr.appendChild(td);

    elementoCorpo.appendChild(tr);

    return;
  }

  for (const item of dados) {

    const tr = document.createElement("tr");

    for (const coluna of COLUNAS[tipo]) {

      const td = document.createElement("td");

      const valor = item[coluna.chave];

      td.textContent =
        valor === null || valor === undefined
          ? "—"
          : valor;

      tr.appendChild(td);
    }

    // =====================================
    // AÇÕES
    // =====================================

    const tdAcoes = document.createElement("td");

    const botaoEditar =
      document.createElement("button");

    botaoEditar.textContent = "Editar";

    botaoEditar.onclick = () =>
      editarRegistro(item);

    const botaoExcluir =
      document.createElement("button");

    botaoExcluir.textContent = "Excluir";

    botaoExcluir.onclick = () =>
      excluirRegistro(item);

    tdAcoes.appendChild(botaoEditar);

    tdAcoes.appendChild(botaoExcluir);

    tr.appendChild(tdAcoes);

    elementoCorpo.appendChild(tr);
  }
}

async function renderizarFormulario(tipo) {

  elementoCampos.innerHTML = "";

  for (const campo of CAMPOS[tipo]) {

    const wrapper = document.createElement("div");

    wrapper.className = "campo";

    const label = document.createElement("label");

    label.htmlFor = `campo-${campo.nome}`;

    label.textContent =
      campo.rotulo + (campo.obrigatorio ? " *" : "");

    wrapper.appendChild(label);

    if (campo.tipo === "select") {

      const select = document.createElement("select");

      select.id = `campo-${campo.nome}`;

      select.name = campo.nome;

      if (campo.obrigatorio) {
        select.required = true;
      }

      const placeholder = document.createElement("option");

      placeholder.value = "";

      placeholder.textContent = "Selecione...";

      select.appendChild(placeholder);

      try {

        const itens = await buscar(campo.origem);

        for (const item of itens) {

          const option = document.createElement("option");

          option.value =
            item.id ??
            item.id_curso ??
            item.id_disciplina ??
            item.id_matricula ??
            item.id_nota ??
            item.id_presenca ??
            item.id_telefone ??
            item.id_email ??
            item.id_endereco;

          option.textContent =
            rotuloItem(campo.origem, item);

          select.appendChild(option);
        }

      } catch (erro) {

        const option = document.createElement("option");

        option.disabled = true;

        option.textContent =
          `Erro ao carregar: ${erro.message}`;

        select.appendChild(option);
      }

      wrapper.appendChild(select);

    } else {

      const input = document.createElement("input");

      input.type = campo.tipo || "text";

      input.id = `campo-${campo.nome}`;

      input.name = campo.nome;

      if (campo.obrigatorio) {
        input.required = true;
      }

      wrapper.appendChild(input);
    }

    elementoCampos.appendChild(wrapper);
  }
}

function rotuloItem(origem, item) {

  if (origem === "professores") {
    return `${item.nome} (id ${item.id})`;
  }

  if (origem === "turmas") {
    return `${item.codigo} - ${item.nome}`;
  }

  if (origem === "cursos") {
    return `${item.nome_curso} (id ${item.id_curso})`;
  }

  if (origem === "disciplinas") {
    return `${item.nome_disciplina} (id ${item.id_disciplina})`;
  }

  if (origem === "alunos") {
    return `${item.nome} (id ${item.id})`;
  }

  return "Registro";
}

function limparMensagem() {

  mensagemFormulario.textContent = "";

  mensagemFormulario.classList.remove(
    "sucesso",
    "erro"
  );
}
function editarRegistro(item) {

  idEditando =
    item.id ||
    item.id_curso ||
    item.id_disciplina ||
    item.id_matricula ||
    item.id_nota ||
    item.id_presenca ||
    item.id_telefone ||
    item.id_email ||
    item.id_endereco;

  for (const campo of CAMPOS[tipoAtual]) {

    const elemento =
      formulario.elements[campo.nome];

    if (!elemento) continue;

    elemento.value =
      item[campo.nome] ?? "";
  }

  elementoTituloFormulario.textContent =
    `Editar ${TITULOS[tipoAtual].lista}`;
}


async function excluirRegistro(item) {

  const id =
    item.id ||
    item.id_curso ||
    item.id_disciplina ||
    item.id_matricula ||
    item.id_nota ||
    item.id_presenca ||
    item.id_telefone ||
    item.id_email ||
    item.id_endereco;

  const confirmar = confirm(
    "Deseja excluir este registro?"
  );

  if (!confirmar) return;

  try {

    const resposta = await fetch(
      `/api/${tipoAtual}/${id}`,
      {
        method: "DELETE"
      }
    );

    if (!resposta.ok) {
      throw new Error(
        `HTTP ${resposta.status}`
      );
    }

    await carregar(tipoAtual);

  } catch (erro) {

    alert("Erro ao excluir.");

    console.error(erro);
  }
}

async function enviarFormulario(evento) {

  evento.preventDefault();

  limparMensagem();

  const dados = {};

  for (const campo of CAMPOS[tipoAtual]) {

    const elemento =
      formulario.elements[campo.nome];

    const valor = elemento.value.trim();

    if (campo.obrigatorio && !valor) {

      mensagemFormulario.textContent =
        `Preencha ${campo.rotulo}.`;

      mensagemFormulario.classList.add("erro");

      elemento.focus();

      return;
    }

    if (valor !== "") {
      dados[campo.nome] = valor;
    }
  }

  const botao =
    formulario.querySelector(
      "button[type=submit]"
    );

  botao.disabled = true;

  try {

    const resposta = await fetch(

      idEditando
        ? `/api/${tipoAtual}/${idEditando}`
        : `/api/${tipoAtual}`,

      {

        method:
          idEditando ? "PUT" : "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify(dados),
      }
    );

    const corpo =
      await resposta.json().catch(() => ({}));

    if (!resposta.ok) {

      throw new Error(
        corpo.erro ||
        `HTTP ${resposta.status}`
      );
    }

    mensagemFormulario.textContent =
      idEditando
        ? "Atualizado com sucesso."
        : "Cadastrado com sucesso.";

    mensagemFormulario.classList.add(
      "sucesso"
    );

    formulario.reset();

    idEditando = null;

    elementoTituloFormulario.textContent =
      TITULOS[tipoAtual].form;

    await carregar(tipoAtual);

  } catch (erro) {

    mensagemFormulario.textContent =
      erro.message;

    mensagemFormulario.classList.add(
      "erro"
    );

  } finally {

    botao.disabled = false;
  }
}


abas.forEach((aba) => {

  aba.addEventListener("click", () => {

    abas.forEach((a) =>
      a.classList.remove("ativa")
    );

    aba.classList.add("ativa");

    carregar(aba.dataset.tipo);
  });
});

botaoRecarregar.addEventListener(
  "click",
  () => carregar(tipoAtual)
);

formulario.addEventListener(
  "submit",
  enviarFormulario
);

carregar("professores");