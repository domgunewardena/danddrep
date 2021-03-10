function colourScores() {

  let scale = [[4,'table-danger'],[4.5,'table-warning'],[5,'table-success']];
  let scoreTDs = Array.from(document.getElementsByClassName('score-td'));
  let scoreCategories = ['food','service','ambience','value']

  scoreTDs.forEach(
    function(scoreTD) {

      let score = scoreTD.textContent;

      // Add titles to zero scores explaining that no guests left a review
      if (score == 0) {

        scoreTD.innerHTML = "<p title = 'No guests left a review'>-</p>"

        for (let i = 0; i < scoreCategories.length; i++) {
          // If score is for a category, show title detailing that specific category
          if (scoreTD.classList.contains(scoreCategories[i])) {
            scoreTD.innerHTML = "<p title = 'No guests left a " + scoreCategories[i] + " score'>-</p>"
          }
        }
      }
      // Add coloured table classes to TDs based on score
      else {
        for (let i = 0; i < scale.length; i++) {
          if (score <= scale[i][0]) {
            scoreTD.classList.add(scale[i][1]);
          }
      }
    }
  });
}

colourScores();
