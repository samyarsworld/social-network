document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);
  // Submit handler for compose email
  document
    .querySelector("#compose-form")
    .addEventListener("submit", send_email);
  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function email_view(id) {
  // Displaying the email
  fetch(`emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      document.querySelector("#emails-view").style.display = "none";
      document.querySelector("#compose-view").style.display = "none";
      document.querySelector("#email-view").style.display = "block";

      // Resetting the view
      document.querySelector("#email-view").innerHTML = "";

      const emailView = document.createElement("div");
      emailView.innerHTML = `
        <ul class="list-group">
          <li class="list-group-item"><strong>From:</strong>${email.sender}</li>
          <li class="list-group-item"><strong>To:</strong>${email.recipients}</li>
          <li class="list-group-item"><strong>Subject:</strong>${email.subject}</li>
          <li class="list-group-item"><strong>Time:</strong>${email.timestamp}</li>
          <li class="list-group-item">${email.body}</li>
        </ul>
        <br>
      `;

      document.querySelector("#email-view").append(emailView);

      // Changing to read
      if (!email.read) {
        fetch(`emails/${id}`, {
          method: "PUT",
          body: JSON.stringify({
            read: true,
          }),
        });
      }

      // Archive
      const btn = document.createElement("button");
      btn.innerHTML = email.archived ? "Unarchive" : "Archive";
      btn.className = email.archived ? "btn btn-success" : "btn btn-danger";
      btn.addEventListener("click", () => {
        fetch(`emails/${id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: !email.archived,
          }),
        }).then((response) => load_mailbox("archive"));
      });

      document.querySelector("#email-view").append(btn);

      // Reply
      const btn_rep = document.createElement("button");
      btn_rep.innerHTML = "Replay";
      btn_rep.className = "btn btn-info ml-2";
      btn_rep.style = "margin-left: 10px;color:white";

      btn_rep.addEventListener("click", () => {
        compose_email();
        document.querySelector("#compose-recipients").value = email.sender;
        document.querySelector(
          "#compose-body"
        ).value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

        let sub = email.subject;
        if (sub.split(" ", 1)[0] != "Re:") {
          sub = "Re: " + sub;
        }
        document.querySelector("#compose-subject").value = sub;
      });

      document.querySelector("#email-view").append(btn_rep);
    });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `
    <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
    <table class="table table-hover">
        <tbody id='emails-view-table'>
        </tbody>
    </table>
  `;

  const hr = document.createElement("hr");
  // Displaying the emails
  fetch(`emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.sort((a, b) => (a.timestamp < b.timestamp ? 1 : -1));
      emails.forEach((email) => {
        const newEmail = document.createElement("tr");
        newEmail.innerHTML = `
            <td class="mail-select">
              <label class="cr-styled">
                <input type="checkbox"><i class="fa"></i>
              </label>
            </td>

            <td>
              ${email.sender}
            </td>

            <td>
              ${email.subject}
            </td>

            <td>
              ${email.body.slice(0, 30)}
            </td>

            <td>
              <i class="fa fa-paperclip"></i>
            </td>

            <td class="">${email.timestamp}</td>
        `;

        // Color for read and unread
        newEmail.style.fontWeight = email.read ? "" : "bold";
        newEmail.style.backgroundColor = email.read ? "#f5f5f5" : "#FFF";

        // Mouse style and hover
        newEmail.style.cursor = "pointer";
        newEmail.addEventListener("mouseover", () => {
          newEmail.style.backgroundColor = "#C9CEF0";
        });
        newEmail.addEventListener("mouseout", () => {
          newEmail.style.backgroundColor = email.read ? "#f5f5f5" : "#FFF";
        });

        document.querySelector("#emails-view-table").append(newEmail);

        // Click and show the details of an email
        newEmail.addEventListener("click", () => {
          email_view(email.id);
        });
      });
    });
}

function send_email(event) {
  // Need this to resolve CORS issue
  event.preventDefault();

  // Grab post data
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch("emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      load_mailbox("inbox");
    });
}
