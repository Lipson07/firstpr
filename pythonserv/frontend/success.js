const storedData = localStorage.getItem('registrationData');
const registrationData = JSON.parse(storedData);

document.addEventListener("DOMContentLoaded", function() {
  
  
    if (storedData) {

      console.log("Данные из localStorage:", registrationData);
  

      const userName = registrationData.name;
      const userPassword = registrationData.password;
  

      const nameParagraph = document.getElementById("user_name");
      const passwordParagraph = document.getElementById("user_password");
  
      if (nameParagraph) {
        nameParagraph.textContent =  " Имя пользователя: " + userName;
      } else {
        console.error("Элемент с id 'user_name' не найден!");
      }
      if (passwordParagraph) {
        passwordParagraph.textContent = "Пароль пользователя: " + userPassword;
      } else {
        console.error("Элемент с id 'user_password' не найден!");
      }
  
      
      console.log("Имя пользователя:", userName);
      console.log("Пароль пользователя:", userPassword);
    } else {
      console.log("Данные в localStorage не найдены.");
    }
  });
