const copy = document.querySelector("#copy");
document.addEventListener("keydown", event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.defaultPrevented) return;
  const relation = { ArrowLeft: "prev", ArrowRight: "next" }[event.key];
  if (relation !== "prev" && relation !== "next") return;
  const destination = document.querySelector(`[rel="${relation}"]`);
  if (destination) {
    event.preventDefault();
    window.location.assign(destination.href);
  }
});

if (copy && navigator.clipboard) {
  copy.hidden = false;
  copy.addEventListener("click", async () => {
    const source = [...document.querySelectorAll(".snippet")]
      .map(block => block.textContent).join("\n\n") + "\n";
    try {
      await navigator.clipboard.writeText(source);
      copy.textContent = "Copied";
    } catch {
      copy.textContent = "Use Download .lean";
    }
  });
}
