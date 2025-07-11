let coll = document.getElementsByClassName("collapsible");
let i;

const x = document.getElementById("send-button");

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function () {
    this.classList.toggle("active");
    let content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
      if (content.children[0].id == "live") {
        content.style.maxHeight = `calc(${content.scrollHeight}px + 25rem)`;
      }
    }
  });
}

let msgs = JSON.parse(localStorage.getItem("messages")) ?? [];

if (msgs) {
  for (let i of msgs) {
    const live = document.getElementById("live");
    const base = document.createElement("div");
    const msg = document.createElement("span");

    if (i.role === "system") {
      base.classList.add("bot");
    } else {
      base.classList.add("you");
    }
    msg.innerHTML = marked.parse(i.content);

    base.appendChild(msg);
    live.appendChild(base);
  }
  document.querySelectorAll("pre code").forEach((block) => {
    const pre = block.parentElement;
    const btn = document.createElement("button");
    btn.innerHTML = "Copy <i class='fa-solid fa-copy'></i>";
    btn.classList.add("copy");
    btn.onclick = () => {
      navigator.clipboard.writeText(block.textContent);
      btn.innerHTML = "Copied <i class='fa-solid fa-check'></i>";
      setTimeout(() => {
        btn.innerHTML = "Copy <i class='fa-solid fa-copy'></i>";
      }, 2500);
    };
    pre.appendChild(btn);
  });
}

async function _() {
  const y = document.getElementById("send");

  if (y.value.length < 2) {
    alert("Please provide text");
  } else if (y.value.startsWith("/")) {
    if (y.value.startsWith("/clear") || y.value.startsWith("/cls")) {
      document.getElementById("live").innerHTML = "";
      // localStorage.setItem("messages", JSON.stringify([]));
      localStorage.removeItem("messages");
      y.focus();
    }
    y.value = "";
  } else {
    y.value = "";
    x.disabled = "disabled";
    y.disabled = "disabled";

    setTimeout(() => {
      const z = document.querySelector("#send");
      z.scrollTo(0, z.scrollHeight + 100);
      z.scrollIntoView({
        behavior: "smooth",
      });
    }, 100);
    

    fetch("/api/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: msgs,
      }),
    })
      .then((res) => {
        return res.json();
      })
      .then((res) => {
        const live = document.getElementById("live");
        const base = document.createElement("div");
        const msg = document.createElement("span");

        base.classList.add("bot");
        msg.innerHTML = marked.parse(res.response);

        // setTimeout(() => {
        //   document.querySelectorAll("pre code").forEach((block) => {
        //     const pre = block.parentElement;
        //     const btn = document.createElement("button");
        //     btn.innerHTML = "Copy <i class='fa-solid fa-copy'></i>";
        //     btn.classList.add("copy");
        //     btn.onclick = () => {
        //       navigator.clipboard.writeText(block.textContent);
        //       btn.innerHTML = "Copied <i class='fa-solid fa-check'></i>";
        //       setTimeout(() => {
        //         btn.innerHTML = "Copy <i class='fa-solid fa-copy'></i>";
        //       }, 2500);
        //     };
        //     // pre.style.position = "relative";
        //     pre.appendChild(btn);
        //   });
        // }, 500);

        base.appendChild(msg);
        live.appendChild(base);
        x.disabled = null;
        y.disabled = null;
        setTimeout(() => {
          const z = document.querySelector("#live");
          z.scrollTo(0, z.scrollHeight + 100);
          z.scrollIntoView({
            behavior: "smooth",
          });
        }, 100);
        msgs.push({
          role: "system",
          content: res.response,
        });
        localStorage.setItem("messages", JSON.stringify(msgs, null, 2));
        y.focus();
      })
      .catch((error) => {
        alert(
          `Error: Please do report to the developer the query and response`,
        );
        console.log(error);
        x.disabled = null;
        y.disabled = null;
        msgs.shift();
      });
  }
}

x.addEventListener("click", (event) => {
  msgs = JSON.parse(localStorage.getItem("messages")) ?? [];

  const y = document.getElementById("send");
  msgs.push({
    role: "user",
    content: y.value,
  });
  const live = document.getElementById("live");
  const base = document.createElement("div");
  const msg = document.createElement("span");

  base.classList.add("you");
  msg.innerHTML = y.value.replace(/\n/gi, "<br>");

  base.appendChild(msg);
  live.appendChild(base);

  _();
});

document.getElementById("send").addEventListener("keyup", (event) => {
  msgs = JSON.parse(localStorage.getItem("messages")) ?? [];

  const y = document.getElementById("send");
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    y.blur();
    msgs.push({
      role: "user",
      content: y.value,
    });
    const live = document.getElementById("live");
    const base = document.createElement("div");
    const msg = document.createElement("span");

    base.classList.add("you");
    msg.innerHTML = y.value.replace(/\n/gi, "<br>");

    base.appendChild(msg);
    live.appendChild(base);
    setTimeout(() => {
      const z = document.querySelector("#live");
      z.scrollTo(0, z.scrollHeight + 100);
      z.scrollIntoView({
        behavior: "smooth",
      });
    }, 100);

    _();
  } else if (event.key === "Tab") {
    event.preventDefault();
    const __ = this;
    const s = __.selectionStart();
    const e = __.selectionEnd();
    __.value = __.value.substring(0, s) + "\t" + value.substring(e);
    __.selectionStart = __.selectionEnd = s + 1;
  }
});

const gpts = [
  {
    name: "gpt-3.5-turbo",
    prov: "OpenAI",
  },
  {
    name: "gpt-4",
    prov: "OpenAI",
  },
  {
    name: "gpt-4o-mini",
    prov: "OpenAI",
  },
  {
    name: "io",
    prov: "OpenAI",
  },
];
