let form = document.querySelector("#join-form");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  let tjsUrl = document.querySelector("#api").value;
  let frameworkData = document.querySelector("#framework").value;
  let attributeData = document.querySelector("#attribute").value;
  let frameworkKey = document.querySelector("#key").value;
  let results = document.querySelector("#results");

  const joinData = `${tjsUrl}FrameworkURI=${frameworkData}&GetDataURL=${attributeData}&FrameworkKey=${frameworkKey}`;

  results.innerHTML = `<button class="btn btn-secondary">
  <a href="${joinData}" target="_blank">
  Link to GeoJSON response
  </a>
  </button>`;
});
