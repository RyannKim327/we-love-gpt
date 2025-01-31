const axios = require("axios");

const a = async () => {
  let { data } = await axios.post("http://127.0.0.1:3000/api/chat", {
    messages: [
      {
        role: "user",
        content: "hello",
      },
    ],
  });
  console.log(data);
};
a();
