const copy = document.querySelector("#copy");
if (copy && navigator.clipboard) {
  copy.hidden = false;
  copy.addEventListener("click", async () => {
    const source = [...document.querySelectorAll(".snippet")]
      .map(block => block.textContent).join("\n\n") + "\n";
    try {
      await navigator.clipboard.writeText(source);
      copy.title = "Copied";
    } catch {
      copy.title = "Download the source code below";
    }
  });
}
