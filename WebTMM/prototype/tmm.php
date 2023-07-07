
<!DOCTYPE html>
<html lang="ko">

<head>
<?php
function h($var) 
{
	if (is_array($var)){
		return array_map('h', $var);
	} else {
		return htmlspecialchars($var, ENT_QUOTES, 'UTF-8');
	}
}

//그래프를 그리는 JavaScript 함수와 그래프를 표시하는 <div> 태그를 생성하는 함수 정의
function makeChartParts($data, $options, $type)
{
	// JavaScript의 함수 이름, <div> 태그의 ID가 중복되지 않도록 하는 일련번호
	static $index=1;

	//그래프의 종류에서 API 로드를 할 때 'packages'를 확인하고 API 로드를 생성
	$package = 'corechart';
	$special_type = array('GeoChart', 'AnnotatedTimeLine','TreeMap', 'OrgChart','Gauge','Table','TimeLine','GeoMap','MotionChart');
	if (in_array($type, $special_type)){
		$package = strtolower($type);
	}
	$load = 'google.load("visualization", "1", {packages:["'.$package.'"]});';

	// 데이터와 옵션을 JSON 형식으로
	$jsData = json_encode($data);
	$jsonOptions = json_encode($options);

	//그래프를 그리는 JavaScript 함수를 생성
	$chart = <<<CHART_FUNC
	 {$load}
	 google.setOnLoadCallback(drawChart{$index});
	 function drawChart{$index}(){
	 	var data = {$jsData};
	 	var chartData = new google.visualization.arrayToDataTable(data);
	 	var options = {$jsonOptions};
	 	var charDiv = document.getElementById('chart{$index}');
	 	var chart = new google.visualization.{$type}(charDiv);
	 	chart.draw(chartData, options);
	 }\n
CHART_FUNC;

	//그래프를 표시하는 <div> 태그를 생성.
	$div = '<div id="chart'.$index.'"></div>';

	$index++; //일련번호에 1을 더함
	return array($chart, $div);
}



//2 x 2 matrix with complex variables
class Matrix{
	var $m;
	function Matrix($q00, $i00, $q01, $i01, $q10, $i10, $q11, $i11){
		$this->m = array(array(array($q00,$i00),array($q01,$i01)),array(array($q10,$i10),array($q11,$i11)));

		//$m[0][0][0] = real
		//$m[0][0][1] = imagenary
	}
	function Mul($target){
		$result = new Matrix(0,0,0,0,0,0,0,0);
		
		for($i=0; $i<2; $i++){
			for($j=0; $j<2; $j++){
				for($k=0; $k<2; $k++){
						for($j2=0; $j2<2; $j2++){
							for($k2=0; $k2<2; $k2++){
								if($k+$k2 == 0){
									$result->m[$i][$j2][0] += $this->m[$i][$j][$k]*$target->m[$j][$j2][$k2];
								} else if ($k+$k2 ==1){
									$result->m[$i][$j2][1] += $this->m[$i][$j][$k]*$target->m[$j][$j2][$k2];
								} else {
									$result->m[$i][$j2][0] -= $this->m[$i][$j][$k]*$target->m[$j][$j2][$k2];
								}
							}
						}
				}
			}
		}

		return $result;
	}
	function Show(){
		echo ' | '.$this->m[0][0][0].' + '.$this->m[0][0][1].' i , '.$this->m[0][1][0].' + '.$this->m[0][1][1].' i | <br>';
		echo ' | '.$this->m[1][0][0].' + '.$this->m[1][0][1].' i , '.$this->m[1][1][0].' + '.$this->m[1][1][1].' i | <br>';
	}

}


class Layer{
	var $d, $n, $k; // parameter
	var $a, $b; // amplitude
	var $m; //transfer matrix with upper layer
	function Layer($surface_depth, $n, $k){
		$this->d = $surface_depth;
		$this->n = $n;
		$this->k = $k;
	}
	function SetTM($uplayer, $wavelength){

		$n1 = ($uplayer->n)*2*PI()/$wavelength;
		$n2 = ($this->n)*2*PI()/$wavelength;
		$k1 = ($uplayer->k)*2*PI()/$wavelength;
		$k2 = ($this->k)*2*PI()/$wavelength;
		$x = $this->d;

		$q = array();

		$emp = exp((-$k1+$k2)*$x);
		$epp = exp((+$k1+$k2)*$x);
		$emm = exp((-$k1-$k2)*$x);
		$epm = exp((+$k1-$k2)*$x);

		$nabs2 = 2*($n2*$n2+$k2*$k2);

		$ap = (($n2+$n1)*$n2+($k2+$k1)*$k2)/$nabs2;
		$am = (($n2-$n1)*$n2+($k2-$k1)*$k2)/$nabs2;
		$bp = (($n2+$n1)*$k2-($k2+$k1)*$n2)/$nabs2;
		$bm = (($n2-$n1)*$k2-($k2-$k1)*$n2)/$nabs2;

		$cpm = cos(($n1-$n2)*$x);
		$spm = sin(($n1-$n2)*$x);
		$cmm = cos((-$n1-$n2)*$x);
		$smm = sin((-$n1-$n2)*$x);		
		$cpp = cos(($n1+$n2)*$x);
		$spp = sin(($n1+$n2)*$x);
		$cmp = cos((-$n1+$n2)*$x);
		$smp = sin((-$n1+$n2)*$x);

		$q[0] = $emp*($ap*$cpm+$bp*$spm);
		$q[1] = $emp*($ap*$spm-$bp*$cpm);
		$q[2] = $epp*($am*$cmm+$bm*$smm);
		$q[3] = $epp*($am*$smm-$bm*$cmm);
		$q[4] = $emm*($am*$cpp+$bm*$spp);
		$q[5] = $emm*($am*$spp-$bm*$cpp);
		$q[6] = $epm*($ap*$cmp+$bp*$smp);
		$q[7] = $epm*($ap*$smp-$bp*$cmp);

		$this->m = new Matrix($q[0],$q[1],$q[2],$q[3],$q[4],$q[5],$q[6],$q[7]);
//		$krt = $krt
	}
}


function Reflect($fm){
	$r10 = $fm->m[1][0][0];
	$i10 = $fm->m[1][0][1];
	$r11 = $fm->m[1][1][0];
	$i11 = $fm->m[1][1][1];

	$rspis = -($r11*$r11+$i11*$i11);
	$result = array();
	$result[0] = ($r10*$r11+$i10*$i11)/$rspis;
	$result[1] = ($i10*$r11-$r10*$i11)/$rspis;

	return $result;
}

?>
<meta charset="UTF-8" />
<style>
A:link {COLOR: black; TEXT-DECORATION: none}
A:visited {COLOR: black; TEXT-DECORATION: none}
A:hover {COLOR: orange; TEXT-DECORATION: underline }
</style>
<a href="./links.html">back<br></a>
<title>TMM-simulation</title>


<?php

	//입력 폼
	echo '<form method="post">';
	echo '
	<dl>';


	$layer = array();
	$depth = 0 ;
	echo '<dd>--------- [0-------------- <input type="hidden" id="layer0" name="layer0" maxlength="50" size="3" value="-1000" required></input> 1000] nm</dd>';
	$layer[0] = new Layer($depth , 1, 0);
	for($i = 0 ; $i<200; $i++){

		if(isset($_POST['layer'.($i+1)]) && $_POST['layer'.$i] != 0 && isset($_POST['nvalue'.$i]) && isset($_POST['kvalue'.$i])){
		$depth += $_POST['layer'.$i];
		$layer[$i] = new Layer($depth , $_POST['nvalue'.$i] , $_POST['kvalue'.$i]);

		echo '<dd>Layer '.($i).' : <input type="range" min="0" max="1000" step="5"  id="layer'.($i+1).'" name="layer'.($i+1).'" maxlength="50" size="3" value="'.$_POST['layer'.($i+1)].'" required></input> '.$_POST['layer'.($i+1)].' nm 
		n : <input type="text" id="nvalue'.$i.'" name="nvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['nvalue'.$i].'" required></input>
		k : <input type="text" id="kvalue'.$i.'" name="kvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['kvalue'.$i].'" required></input></dd>';

		} else {
			echo '<dd> <input type="hidden" id="layer'.($i+1).'" name="layer'.($i+1).'" maxlength="50" size="3" value="0" required></input>
			<input type="hidden" id="nvalue'.$i.'" name="nvalue'.$i.'" maxlength="50"  size="3" value="1" required></input>
			<input type="hidden" id="kvalue'.$i.'" name="kvalue'.$i.'" maxlength="50"  size="3" value="0" required></input></dd>';
			break; 
		}

	}

	echo '<dd><input type="submit" name="submit" data-inline="true" data-mini="true" value="Confirm"></dd>
	</dl>
	</form>

	';

	//특수 입력 폼1 (전전 layer 생성)

	if(isset($_POST['layer'.($i-2)]) && isset($_POST['nvalue'.($i-3)]) && isset($_POST['kvalue'.($i-3)])){
	echo '<form method="post">';
	echo '
	<dl>';

	echo '<dd><input type="hidden" id="layer0" name="layer0" maxlength="50" size="3" value="-1000" required></input></dd>';

	for($i = 0 ; $i<200; $i++){

		if(isset($_POST['layer'.($i+1)]) && $_POST['layer'.$i] != 0 && isset($_POST['nvalue'.$i]) && isset($_POST['kvalue'.$i])){

					if($_POST['layer'.($i+1)]== 0 ){
		echo '<dd><input type="hidden" min="0" max="1000" step="5"  id="layer'.($i+1).'" name="layer'.($i+1).'" maxlength="50" size="3" value="'.$_POST['layer'.($i-1)].'" required></input>
		<input type="hidden" id="nvalue'.$i.'" name="nvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['nvalue'.($i-2)].'" required></input>
		<input type="hidden" id="kvalue'.$i.'" name="kvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['kvalue'.($i-2)].'" required></input></dd>';

					}	else {
		echo '<dd><input type="hidden" min="0" max="1000" step="5"  id="layer'.($i+1).'" name="layer'.($i+1).'" maxlength="50" size="3" value="'.$_POST['layer'.($i+1)].'" required></input>
		<input type="hidden" id="nvalue'.$i.'" name="nvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['nvalue'.$i].'" required></input>
		<input type="hidden" id="kvalue'.$i.'" name="kvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['kvalue'.$i].'" required></input></dd>';
						}

		} else {

			echo '<dd> <input type="hidden" id="layer'.($i+1).'" name="layer'.($i+1).'" maxlength="50" size="3" value="'.$_POST['layer'.($i-1)].'" required></input>
			<input type="hidden" id="nvalue'.$i.'" name="nvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['nvalue'.($i-2)].'" required></input>
			<input type="hidden" id="kvalue'.$i.'" name="kvalue'.$i.'" maxlength="50"  size="3" value="'.$_POST['kvalue'.($i-2)].'" required></input></dd>';
			break; 
		}

	}

	echo '<dd><input type="submit" name="submit" data-inline="true" data-mini="true" value="Periodic"></dd>
	</dl>
	</form>

	';
	}


/*
if(isset($_POST['layer'.$i]) && isset($_POST['nvalue'.$i]) && isset($_POST['kvalue'.$i])){
	$surface = new Layer($_POST['layer'.$i] , $_POST['nvalue'.$i] , $_POST['kvalue'.$i]);
} else {$surface = new Layer(0, 1.0, 0);}
*/

$reflect = array(array('Wavelength', 'R', 'T'));


for($i=390;$i<831;$i++){

$fm = new Matrix(1,0,0,0,0,0,1,0);

$n_layer = count($layer);
for($j=1;$j<$n_layer;$j++){
	$layer[$j]->SetTM($layer[$j-1], $i);
	$fm = $layer[$j]->m->Mul($fm);
}
//find fm end 


$reflect_r = Reflect($fm);
$ramp = ($reflect_r[0]*$reflect_r[0]+$reflect_r[1]*$reflect_r[1]);
/*
if($reflect_r[0]==0){
	$phase = 0;
} else if($reflect_r[0]>0){
	$phase = (180/PI())*atan($reflect_r[1]/$reflect_r[0]);
}	else {$phase = (180/PI())*atan($reflect_r[1]/$reflect_r[0])+180; }
*/
$t_r = $fm->m[0][0][0]+($fm->m[0][1][0])*$reflect_r[0]-($fm->m[0][1][1])*$reflect_r[1]; 
$t_i = $fm->m[0][0][1]+($fm->m[0][1][1])*$reflect_r[0]+($fm->m[0][1][0])*$reflect_r[1];
$tamp = (($layer[$n_layer-1]->n)/($layer[0]->n))*($t_r*$t_r+$t_i*$t_i);

$reflect[] = array($i, $ramp, $tamp);

}



?>


<?php


// 그래프의 옵션
$options = array(
	'title' =>'Spectrum',
	'titleTextStyle' => array('fontSize'=>16),
	'series' => array(1=>array('targetAxisIndex'=>1)), //세로 축을 2축화
	'width' => 550, 'height'=> 340, //폭, 높이
	'chartArea'=> array('width'=>460, 'height'=>240), //차트 영역
	'legend' => array('position'=>'in', 'alignment'=>'start') //범례
	);

//그래프의 유형(꺾은선)
$type = 'LineChart';

//그래프를 생성하는 JavaScript 함수와 표시하는 <div> 태그를 생성.
list($chart, $chart_div) = makeChartParts($reflect, $options, $type);

?>

<p>

<script src = "https://www.google.com/jsapi"></script>
<script>
<?php
//그래프를 생성하는 함수를 표시
echo $chart;
?>
</script>


<?php

$red = 0;
$green = 0;
$blue = 0;

$t_red = 0;
$t_green = 0;
$t_blue = 0;

//cie 불러오기
$cie = array();
$fp = fopen("./cie.csv","r");
while($row = fgetcsv($fp)) $cie[] = $row;
for($i=0;$i<count($cie);$i++){

$red += 1.0*$cie[$i][1]*$reflect[$i+1][1];
$green += 1.0*$cie[$i][2]*$reflect[$i+1][1];
$blue += 1.0*$cie[$i][3]*$reflect[$i+1][1];

$t_red += 1.0*$cie[$i][1]*$reflect[$i+1][2];
$t_green += 1.0*$cie[$i][2]*$reflect[$i+1][2];
$t_blue += 1.0*$cie[$i][3]*$reflect[$i+1][2];

}

//CIE 좌표 구하기
if(($red+$green+$blue)==0){
$x = '';
$y = '';
} else {
$x = $red/($red+$green+$blue);
$y = $green/($red+$green+$blue);
}

echo 'CIE axis values <br>'; 
echo 'X = '.$x.'<br>'; 
echo 'Y = '.$y.'<br>';

//디지털 색 표현 
$max = 113.04232;
$color256 = 255/$max;


echo '
   <script type="application/javascript"> 
    function draw() { 
      var canvas = document.getElementById("canvas"); 
      if (canvas.getContext) { 
        var ctx = canvas.getContext("2d"); 

        ctx.fillStyle = "rgb('.floor($color256*$red).','.floor($color256*$green).','.floor($color256*$blue).')"; 
        ctx.fillRect (10, 10, 100, 100); 
 		
 		ctx.fillStyle = "rgb('.floor($color256*$t_red).','.floor($color256*$t_green).','.floor($color256*$t_blue).')"; 
        ctx.fillRect (10, 150, 100, 100); 
      } 

     var canvas2 = document.getElementById("canvas2"); 
      if (canvas2.getContext) { 
        var ctx = canvas2.getContext("2d"); 

       for(red=0; red<25; red++){
       	for(green=0; green<25; green++){
       		for(blue=0; blue<25; blue++){

       		var red2 = red*10;
       		var green2 = green*10;
       		var blue2 = blue*10;

       		ciex = red2/(red2+green2+blue2);
       		ciey = green2/(red2+green2+blue2);

        ctx.fillStyle = "rgb("+red2+","+green2+","+blue2+")"; 
        ctx.fillRect (270*ciex, 270-270*ciey, 20, 20); 
 
 		}}}

 		    var red2 = '.floor($color256*$red).';
       		var green2 = '.floor($color256*$green).';
       		var blue2 = '.floor($color256*$blue).';

       		ciex = red2/(red2+green2+blue2);
       		ciey = green2/(red2+green2+blue2);
        ctx.fillStyle = "rgb(0,0,0)"; 
        ctx.fillRect(270*ciex, 270-270*ciey, 10, 10); 

        	var t_red2 = '.floor($color256*$t_red).';
       		var t_green2 = '.floor($color256*$t_green).';
       		var t_blue2 = '.floor($color256*$t_blue).';

       		t_ciex = t_red2/(t_red2+t_green2+t_blue2);
       		t_ciey = t_green2/(t_red2+t_green2+t_blue2);
        ctx.fillStyle = "rgb(150,150,150)"; 
        ctx.fillRect(270*t_ciex, 270-270*t_ciey, 10, 10); 

      } 

    } 

     </script> 
';


?>
</head>

<?/*
echo '</head>
	<body bgcolor="rgb(0,0,0)">';

echo '</head>
	<body bgcolor="rgb('.$red*$color256.','.$green*$color256.','.$blue*$color256.')">';
*/
?>

<body onload="draw()">

<div>
<?php
//적당한 위치에 그래프를 표시하는 <div> 태그를 배치
echo $chart_div;
?>
</div>



<p>

<canvas id="canvas" width="250" height="300"></canvas>
<canvas id="canvas2" width="300" height="300"></canvas>

</body>
</html>