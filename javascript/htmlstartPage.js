
function exitApplication() {
  // you cannot close the current window 
  // you can only close a window that is opened by yourself.

  // solution: set a message  
  document.title = "Closed";
  document.body.innerHTML = "<h1 class='center'>Application closed</h1>";

  // stop the python http server
  asyncExitApplication();

  // you cannot change the url with an empty string
  // window.location.replace( '' );
}

async function asyncExitApplication() {
  try {
     url = '?prog=exit';

     config = {
        method: 'GET',
     }
     // this gives an error: Uncaught (in promise) TypeError: NetworkError when attempting to fetch resource. 
     // Server is stopped and give no response back 
     fetch( url, config );
  } catch(err) {
    // alert( 'Error exit application ' + err );
  }
}
