var nodemailer = require('nodemailer');

var transporter = nodemailer.createTransport({
  host: 'smtp.163.com',
  secureConnection: true,
  auth: {
    user: 'giraffe0813@163.com',
    pass: 'giraffe930813'
  },
  port: 465
});

var mailOptions = {
  from: 'giraffe0813@163.com',
  to: 'yemengying1993@foxmail.com',
  subject: 'Hello World 🐱 ✔',
  html: `
    <h2>您有一条新的消息</h2>
    <a href="http://yemengying.com">博主回复了你的评论，点击查看</a>
    <p>来自：<a href="http://yemengying.com">yemengying.com</a></p>
  `,
  connectionTimeout: 500
};

transporter.sendMail(mailOptions, function(error, info){
  if(error){
    return console.log(error);
  }
  console.log('Message sent: ' + info.response);
});

