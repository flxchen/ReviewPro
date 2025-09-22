//generate review
const generateBtn = document.getElementById("generateBtn");
const spinner = document.getElementById("spinner");
const copyBtn = document.getElementById("copyButton");
const form = document.getElementById("reviewForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Prevent submission if invalid or over limit
  if (!form.checkValidity()) {
    form.classList.add("was-validated");    
    return;
  }

  form.classList.add("was-validated");
  generateBtn.disabled = true;
  spinner.style.display = "inline";
  const data = {
    review: document.getElementById("review").value,
    tone: document.getElementById("tone").value,
    words: document.getElementById("words").value,
    instruction: document.getElementById("instruction").value,
  };
  try {
    //send to backend
    const response = await fetch("/generate-reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const result = await response.json();
    if (!response.ok) {
      document.getElementById("replyOutput").textContent = result.error;
    } else {
      document.getElementById("replyOutput").textContent = result.reply;
    }
    copyBtn.disabled = false;
  } catch (error) {
    console.error("Error fetching reply:", error);
    document.getElementById("replyOutput").textContent =
      "⚠️ Unable to generate reply. Please try again later.";
  } finally {
    generateBtn.disabled = false;
    spinner.style.display = "none";
  }
});

//copy reply
copyBtn.addEventListener("click", () => {
  const replyText = document.getElementById("replyOutput").textContent;
  const cpboard = navigator.clipboard;
  if (cpboard && cpboard.writeText) {
    cpboard.writeText(replyText).then(() => showCopy());
  } else {
    fallbackCopy(replyText);
  }
});

function showCopy() {
  copyBtn.textContent = "Copied!";
  copyBtn.classList.remove("btn-outline-primary");
  copyBtn.classList.add("btn-success");

  setTimeout(() => {
    copyBtn.textContent = "Copy Reply";
    copyBtn.classList.remove("btn-success");
    copyBtn.classList.add("btn-outline-primary");
  }, 1500);
}
//alternative copy for mobile
function fallbackCopy(text) {
  const temp = document.createElement("textarea");
  temp.value = text;
  temp.style.position = "fixed"; // prevent scrolling to bottom
  temp.style.opacity = "0";
  document.body.appendChild(temp);
  temp.focus();
  temp.select();
  try {
    document.execCommand("copy");
    showCopy();
  } catch (err) {
    alert("Failed to copy. Please copy manually.");
  }
  document.body.removeChild(temp);
}
