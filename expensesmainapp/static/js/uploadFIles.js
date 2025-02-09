function form_d(e) {
  e.preventDefault();
  console.log("hope you are working ");
  var formData = new FormData(e.target);
  //each form id is represented by formID the value changes depending on the form submitted
  const form_values = Object.fromEntries(formData);
  console.log(form_values);
  //   id = form_values.id;
  //   title = form_values.title;

  //   published = form_values.published;
  //   file = form_values.file;
  //   var file = {
  //     lastModified: file.lastModified,
  //     lastModifiedDate: file.lastModifiedDate,
  //     name: file.name,
  //     size: file.size,
  //     type: file.type,
  //   };
  //   console.log("file", file);
  //   if (published == "on") {
  //     published = true;
  //   } else {
  //     published = false;
  //   }
  //   const post_process = "form_submit";
  //   const url = "/dashboard/";

  //   file = form_values.file;
  //   let formDa = new FormData();
  //   formDa.append("file", file);
  //   formDa.append("title", title);
  //   formDa.append("body", body);
  //   formDa.append("published", published);
  //   formDa.append("id", id);
  //   formDa.append("formId", formID);
  //   formDa.append("process", post_process);

  //   fetch(url, {
  //     method: "POST",
  //     headers: {
  //       "X-CSRFToken": csrftoken,
  //     },
  //     body: formDa,
  //   }).then((response) => {
  //     response.json();
  //     if (response.status == 200) {
  //       location.reload();
  //     }
  //   });
}
