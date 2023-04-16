document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .getElementById("ai-btn")
    .addEventListener("click", () => ai_generate());
  // document
  //   .getElementById("find-btn")
  //   .addEventListener("click", () => find_posts());
});

// Create dynamic filter later
// const find_posts = () => {
//   const query = document.getElementById("prompt").value;
//   const feed = document.querySelector(".feed");
//   for (let i = 0; i < 10; i++) {
//     const div = document.createElement("div");
//     div.innerHTML = "meh";

//     feed.append(div);
//   }
// };

let loadInterval;

function loader(element) {
  element.textContent = "";
  loadInterval = setInterval(() => {
    element.textContent += ".";

    if (element.textContent === "....") {
      element.textContent = "";
    }
  }, 300);
}

function type(element, response) {
  let index = 0;
  let interval = setInterval(() => {
    if (index < response.length) {
      element.innerHTML += response[index];
      index++;
    } else {
      clearInterval(interval);
    }
  }, 30);
}

const ai_generate = async () => {
  const prompt = document.getElementById("prompt").value;

  if (prompt) {
    const aiResponse = document.getElementById("ai-response");
    aiResponse.innerHTML = "...";

    loader(aiResponse);

    try {
      const response = await fetch("ai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      clearInterval(loadInterval);
      aiResponse.innerHTML = "";

      if (response.ok) {
        const data = await response.json();
        // const parsedData = data.bot.trim();
        type(aiResponse, data.response);
      } else {
        aiResponse.innerHTML = "Something went wrong, please try again.";
      }
    } catch (error) {
      console.log(error);
    }
  }
};
