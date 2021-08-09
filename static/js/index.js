let form = document.querySelector("#join-form");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  let tjsUrl = document.querySelector("#apiurl").value;
  let frameworkData = document.querySelector("#frameworkurl").value;
  let attributeData = document.querySelector("#attributeurl").value;
  let frameworkKey = document.querySelector("#frameworkkey").value;
  let attributeKey = document.querySelector("#attributekey").value;
  let results = document.querySelector("#results");

  const joinData = `${tjsUrl}FrameworkURI=${frameworkData}&GetDataURL=${attributeData}&FrameworkKey=${frameworkKey}&AttributeKey=${attributeKey}`;

  results.innerHTML = `<strong><div>👇🏽</div><div><a href="${joinData}" target="_blank">Link to GeoJSON response</a></div></strong>`;
});
