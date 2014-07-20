var Score = function () {

	var container = document.createElement( 'div' );
	container.id = 'scoreboard';
	container.style.cssText = 'width:500px;height:15px;opacity:0.9;cursor:pointer';

	var scoreDiv = document.createElement( 'div' );
	scoreDiv.id = 'score';
	scoreDiv.style.cssText = 'padding:0 0 3px 3px;text-align:center;background-color:#002';
	container.appendChild( scoreDiv );
	
	var scoreText = document.createElement( 'div' );
	scoreText.id = 'scoreText';
	scoreText.style.cssText = 'color:#0ff;font-family:Segoe UI, Helvetica, Ubuntu, sans-serif;font-size:40px;font-weight:bold;line-height:35px';
	scoreText.innerHTML = 'SCORE';
	scoreDiv.appendChild( scoreText );

	
	return {

		domElement: container,

		update: function (actual_score) {

			scoreText.textContent = 'SCORE : ' + actual_score;
		}

	}

};