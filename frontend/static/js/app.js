/**
 * 口腔智植-模拟诊所 前端
 * 展示窗口初始显示欢迎语；打字输入与文件提交分开；发送后禁用输入直至后端回复展示完毕。
 */

const API_BASE = "http://127.0.0.1:8000/api/v1";

const WELCOME_TEXT = "欢迎来到智植诊所！";

function getDisplayArea() {
  return document.getElementById("display-area");
}

function getTextInput() {
  return document.getElementById("text-input");
}

function getBtnSendText() {
  return document.getElementById("btn-send-text");
}

function getFileInput() {
  return document.getElementById("file-input");
}

function getBtnUpload() {
  return document.getElementById("btn-upload");
}

/** 在展示窗口末尾换行追加一行文字 */
function appendDisplayLine(text) {
  const el = getDisplayArea();
  const current = el.innerHTML.trim();
  const line = document.createElement("div");
  line.className = "line";
  line.textContent = text;
  el.appendChild(line);
  el.scrollTop = el.scrollHeight;
}

/** 设置展示区域初始内容（仅保留欢迎语） */
function initDisplay() {
  const el = getDisplayArea();
  el.innerHTML = "";
  const line = document.createElement("div");
  line.className = "line";
  line.textContent = WELCOME_TEXT;
  el.appendChild(line);
}

/** 禁用所有输入与按钮 */
function setInputsDisabled(disabled) {
  getTextInput().disabled = disabled;
  getBtnSendText().disabled = disabled;
  getFileInput().disabled = disabled;
  getBtnUpload().disabled = disabled;
}

async function submitText(text) {
  const res = await fetch(`${API_BASE}/contents`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: "text", text_content: text }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

(function init() {
  initDisplay();

  const textInput = getTextInput();
  const btnSendText = getBtnSendText();
  const fileInput = getFileInput();
  const btnUpload = getBtnUpload();

  btnSendText.addEventListener("click", async () => {
    const text = textInput.value.trim();
    if (!text) return;
    setInputsDisabled(true);
    appendDisplayLine(text);
    textInput.value = "";
    try {
      const data = await submitText(text);
      const reply = data.reply_message || "我们医生组先想想";
      appendDisplayLine(reply);
    } catch (e) {
      appendDisplayLine("发送失败: " + e.message);
    } finally {
      setInputsDisabled(false);
    }
  });

  btnUpload.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) {
      alert("请先选择文件");
      return;
    }
    setInputsDisabled(true);
    try {
      const data = await uploadFile(file);
      appendDisplayLine("[已提交文件: " + file.name + "]");
      const reply = data.reply_message || "我们医生组先想想";
      appendDisplayLine(reply);
      fileInput.value = "";
    } catch (e) {
      appendDisplayLine("提交失败: " + e.message);
    } finally {
      setInputsDisabled(false);
    }
  });
})();
