const form = document.querySelector("form");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const tjsapiUrl = document.querySelector("#tjs-api");
  const frameworkDataUrl = document.querySelector("#framework-data");
  const attributeDataUrl = document.querySelector("#attribute-data");
  const frameworkKey = document.querySelector("#framework-key");
  const joinData =
    "tjsapiUrl.value + frameworkDataUrl.value + attributeDataUrl.value + frameworkKey.value";
  console.log(frameworkDataUrl.value);
});
