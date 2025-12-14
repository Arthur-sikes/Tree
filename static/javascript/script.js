function showMTN() {
  document.getElementById("mtnSection").style.display = "block";
}

function comingSoon() {
  alert("This network is coming soon.");
}

function openPayment() {
  document.getElementById("paymentBox").style.display = "block";
  detectDevice();
}

function copyText(text) {
  navigator.clipboard.writeText(text);
  alert("Copied: " + text);
}

function detectDevice() {
  const ua = navigator.userAgent.toLowerCase();
  const notice = document.getElementById("deviceNotice");
  const dialBtn = document.getElementById("dialBtn");

  if (ua.includes("iphone") || ua.includes("ipad")) {
    notice.innerHTML =
      "📱 <b>iPhone user:</b><br>" +
      "Please dial <b>*170#</b> manually.<br>" +
      "Choose <b>Transfer Money</b>, enter the number above, confirm name, and use reference <b>BUNDLE</b>.";
    dialBtn.style.display = "none";
  } else {
    notice.innerHTML =
      "📱 <b>Android user:</b><br>" +
      "Click the button below to dial *170#. If it doesn’t work, dial manually.";
    dialBtn.style.display = "block";
  }
}

function dialUSSD() {
  window.location.href = "tel:*170#";
}

function openWhatsApp() {
  window.location.href =
    "https://wa.me/233533833889?text=Hello%20I%20have%20paid%20for%20a%20bundle.%20Reference:%20BUNDLE";
}
