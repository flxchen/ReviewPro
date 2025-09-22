//close form
const modal = document.getElementById("feedbackModal");
const btn = document.getElementById("feedbackBtn");
const span = document.getElementById("closeModal");

btn.onclick = () => (modal.style.display = "block");
span.onclick = () => (modal.style.display = "none");
window.onclick = (event) => {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

//submit feedback
const feedbackForm = document.getElementById("feedbackForm");
feedbackForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!feedbackForm.checkValidity()) {
    feedbackForm.classList.add("was-validated");    
    return;
  }
  feedbackForm.classList.add("was-validated");
  const data = {
    enjoy: feedbackForm.enjoy.value,
    improvement: feedbackForm.improvement.value,
    pay: feedbackForm.pay.value,
    payment_type: feedbackForm.payment_type.value,
    amount: feedbackForm.amount.value
  };

  const submitBtn = document.getElementById("feedbackSubmitBtn");
  submitBtn.disabled = true;
  submitBtn.textContent = "Submitting...";

  try {
    const response = await fetch("/submit-feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
      alert(result.error || "Failed to submit feedback.");
    } else {
      alert(result.message || "Feedback submitted successfully.");
      feedbackForm.reset();
    }
  } catch (err) {
    console.error(err);
    alert("An error occurred while submitting feedback.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Submit Feedback";
    modal.style.display = "none";
  }
});