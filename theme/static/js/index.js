document.getElementById('submit-btn').addEventListener('click', function(e) {
  e.preventDefault(); // Prevent the default button action
  
  document.getElementById('loading-animation').classList.remove('hidden');  
  
  const formData = new FormData();
  const imageFile = document.getElementById('file-input').files[0];    
  formData.append('file', imageFile);
  const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
    
  fetch('https://magicframeapp.onrender.com/upload/', {
  // fetch('http://127.0.0.1:8000/upload/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrftoken,
    },      
  })
 
  .then(response => {
      if (response.ok) {        
        document.getElementById('loading-animation').classList.add('hidden');  
        document.getElementById('card_info_block').classList.remove('hidden');
      }        
      return response.json();
    })
  .then(data => {

    const responseElementCardName = document.getElementById('frame_card_name');
    responseElementCardName.innerHTML = `${data['frame_card_name']}`;

    const responseElemenCardImage = document.getElementById('frame_card_image');
    responseElemenCardImage.src = `${data['frame_card_image']}`;

    const responseElementCardRulings = document.getElementById('frame_card_rulings');
    data['frame_card_rulings'].forEach(element => {
      responseElementCardRulings.innerHTML += 
      `<li>${element['publish_at']}: ${element['comment']}</li>`;
    });

    const reponseElementTcgPrice = document.getElementById('frame_tcg_purcase_link');
    reponseElementTcgPrice.href = `${data['frame_tcg_purcase_link']}`;    

    const reponseElementUsdPrice = document.getElementById('frame_usd_price');
    reponseElementUsdPrice.innerHTML = `${data['frame_usd_price']}`;

    const reponseElementUsdFoilPrice = document.getElementById('frame_usd_foil_price');
    reponseElementUsdFoilPrice.innerHTML = `${data['frame_usd_foil_price']}`;

    const reponseElementUsdEtchedPrice = document.getElementById('frame_usd_etched_price');
    reponseElementUsdEtchedPrice.innerHTML = `${data['frame_usd_etched_price']}`;

    const responseElementEurPrice = document.getElementById('frame_eur_price');
    responseElementEurPrice.innerHTML = `${data['frame_eur_price']}`;

    const reponseElementEurFoilPrice = document.getElementById('frame_eur_foil_price');
    reponseElementEurFoilPrice.innerHTML = `${data['frame_eur_foil_price']}`;

  })
  .catch(error => console.error('Error:', error));  
});
