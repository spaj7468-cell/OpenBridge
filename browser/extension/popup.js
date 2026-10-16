const captureButton = document.getElementById("capture-tab");
const copyButton = document.getElementById("copy-context");
const titleNode = document.getElementById("tab-title");
const urlNode = document.getElementById("tab-url");
const statusTitle = document.getElementById("status-title");
const statusText = document.getElementById("status-text");
const feedback = document.getElementById("feedback");

let capturedContext = null;

captureButton.addEventListener("click", async () => {
  statusTitle.textContent = "Capturing active tab…";
  statusText.textContent = "Reading only the active tab title and URL.";
  feedback.textContent = "";
  try {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const tab = tabs[0];
    if (!tab) throw new Error("No active tab was found.");
    capturedContext = {
      title: String(tab.title || "Untitled page"),
      url: String(tab.url || "")
    };
    titleNode.textContent = capturedContext.title;
    urlNode.textContent = capturedContext.url || "URL unavailable for this tab.";
    copyButton.disabled = !capturedContext.url;
    statusTitle.textContent = "Tab captured";
    statusText.textContent = "Nothing was sent to a server.";
    feedback.textContent = "Ready to copy. Page contents and browsing history were not read.";
  } catch (error) {
    capturedContext = null;
    copyButton.disabled = true;
    statusTitle.textContent = "Could not capture tab";
    statusText.textContent = "Open a regular webpage and try again.";
    feedback.textContent = String(error?.message || error);
  }
});

copyButton.addEventListener("click", async () => {
  if (!capturedContext) return;
  const text = "Current browser tab\nTitle: " + capturedContext.title + "\nURL: " + capturedContext.url;
  try {
    await navigator.clipboard.writeText(text);
    feedback.textContent = "Tab context copied. Paste it into your AI chat when you choose.";
  } catch {
    feedback.textContent = "Clipboard access failed. Select and copy the title and URL manually.";
  }
});
