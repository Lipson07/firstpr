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
        nameParagraph.textContent =    userName;
      } else {
        console.error("Элемент с id 'user_name' не найден!");
      }
      
  
      
      console.log("Имя пользователя:", userName);
      console.log("Пароль пользователя:", userPassword);
    } else {
      console.log("Данные в localStorage не найдены.");
    }
  });
