var decide=0;
	var b_array = ["sample"];
	var system_array=["b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","b11","b12","b13","b14","b15","b16"];
	var sys_count=1;
	var doc;
	//alert (system_array.length);
	
// alert("Script is working");

	var player1=prompt("First Player Name: ");
 	var player2=prompt("Second Player Name :<Skip this step by Hit Enter>").toLowerCase();
 	if (player2=='')
 		player2='system'

 	
			var player1_symbol=',';
			var player2_symbol='.';

		$(document).ready(function(){


$('#circle1').hide();
$('#system').hide();


			document.getElementById("id_player1").innerHTML =player1;
			//document.getElementById("sym_p1").innerHTML =player1_symbol;
			document.getElementById("id_player2").innerHTML =player2;
			//document.getElementById("sym_p2").innerHTML =player2_symbol;
//			alert("Document ready");

			
	$(".unclicked").click(function() {
		
		 
//`	      alert("Button clicked");
			    var bid=this.id;
			    
			    var imp = b_array.indexOf(bid);
			     if(imp==-1)  // IF THE BUTTON  IS NOT PRESENT IN THE ARRAY 
			   {
			   	decide++; //alert("Decide :"+decide); 
			   	b_array.push(bid);
			   	if (player2=='system'){
			   		if(sys_count<8)
			   		{ 				//alert("System_Count"+sys_count);
			   			           document.getElementById('circle').style.display = 'block';
			   			           document.getElementById('system').style.display = 'none';
			             	 	   document.getElementById('circle1').style.display = 'none';
			             	 	   document.getElementById(bid).style.backgroundImage = "url('images/player1.png')";
			             	 	   document.getElementById(bid).value =',';
			             	 	   sys_count++;
			             	 	   //alert("System count "+sys_count);
			                       get_win(',');
			                       //alert(x);
			                       system_turn();

			                      
			        }
			   		else{ alert("Match Draw!!"); window.location.reload();}




			   	}
			   
			   	            else if ((decide%2==0))
			             	 {
			   
			             	 	
			             	 	   document.getElementById('circle').style.display = 'block';
			             	 	   document.getElementById('circle1').style.display = 'none';
			             	 	   document.getElementById(bid).style.backgroundImage = "url('images/player2.png')";
			             	 	

			                      document.getElementById(bid).value ='.';
			                      get_win('.');
			                      if(decide==15)
			    	              {
			    		          alert("Match Draw!!");
			                      window.location.reload();
			                       }
			                      
			                  } 
			                   else if(decide==15)
			    	           {
			    		         alert("Match Draw!!");
			                      window.location.reload();
			                   }
			                   
			        	  else if(decide<=14)
			        	     {// IF THE SECOND PLAYER IS SYSTEM IT SHOULD DO THE FOLLOWING!!

			        	 		document.getElementById('circle1').style.display = 'block';
			         			document.getElementById('circle').style.display = 'none';
			         			document.getElementById(bid).style.backgroundImage = "url('images/player1.png')";
			         			document.getElementById(bid).value =',';
			         			get_win(','); 
			          			}
			          			



			        	     
			         			
			              

			    }
			       else {
			       	alert("Already Clicked !!");
			       decide-=1;
			   }
                      
			    		
			   
			   
});// End of click function

	}); // End of document Function 

function get_random_element() // GENERATES A RANDOM \
{
	if(b_array.length>5)
	{
	var pos1=p_check('b1','b2','b3','b4');
	//alert("pos1 :"+pos1); break;
	var pos2=p_check('b5','b6','b7','b8');
    var pos3=p_check('b9','b10','b11','b12');
    var pos4=p_check('b13','b14','b15','b16');
    var pos5=p_check('b1','b5','b9','b13');
    var pos6=p_check('b2','b6','b10','b14');
    var pos7=p_check('b3','b7','b11','b15');
    var pos8=p_check('b4','b8','b12','b16');
    var pos9=p_check('b1','b6','b11','b16'); //diagonal win
    var pos10=p_check('b4','b7','b10','b13'); //diangonal win 
    if((pos1!=0)&&((b_array.indexOf(pos1))==-1)) { return pos1;}
    else if((pos2!=0)&&((b_array.indexOf(pos2))==-1)) { return pos2;}
     else if((pos3!=0)&&((b_array.indexOf(pos3))==-1)) { return pos3;}
     else if((pos4!=0)&&((b_array.indexOf(pos4))==-1)) { return pos4;}
     else if((pos5!=0)&&((b_array.indexOf(pos5))==-1)) { return pos5;}
     else if((pos6!=0)&&((b_array.indexOf(pos6))==-1)) { return pos6;}
     else if((pos7!=0)&&((b_array.indexOf(pos7))==-1)) { return pos7;}
     else if((pos8!=0)&&((b_array.indexOf(pos8))==-1)) { return pos8;}
     else if((pos9!=0)&&((b_array.indexOf(pos9))==-1)) { return pos9;}
     else if((pos10!=0)&&((b_array.indexOf(pos1))==-1)) { return pos10;}
     else{
	
	      var x = Math.floor((Math.random()*16));
  
	
	//alert("Random function called!");
	      var sys_bid = system_array[x];
	
	      return sys_bid;
	}}


 else{
	
	      var x = Math.floor((Math.random()*16));
  
	
	//alert("Random function called!");
	      var sys_bid = system_array[x];
	
	      return sys_bid;
	}	
}

function system_turn()
{  
	//var b=bid;
	
    document.getElementById('system').style.display = 'block';
     //if (b==0) 
     	temp_bid=get_random_element();
     	//alert("temp ID :"+temp_bid);
     //else temp_bid=b;
  	//alert("System turn called!!");
  	
	var temp_index=b_array.indexOf(temp_bid);
	//alert("temp index !! : "+temp_index);
	if (temp_index=='-1') // ELEMENT IS NOT PRESENT IN THE ARRAY
	{
		
		  b_array.push(temp_bid);
		 //alert("Value added!"+temp_bid);
		  //alert(b_array);
		  document.getElementById('circle1').style.display = 'none';
		  document.getElementById('circle').style.display = 'block';
		  document.getElementById(temp_bid).style.backgroundImage ="url('images/player2.png')";
		  document.getElementById(temp_bid).value ='.';
		  get_win('.'); 
		  
     }
     else
     {
     	//alert("Else part called!");
     	system_turn();
     }
 }//}




function p_check(a,b,c,d)
{
 var b1=document.getElementById(a).value;
 var b2=document.getElementById(b).value;
 var b3=document.getElementById(c).value;
 var b4=document.getElementById(d).value;
if((b1==b2)&&(b2==b3)&&(b3==b4)) { //alert("Wining"); 
return 0;}
else if((b1==b2)&&(b2==b3)) { //alert("the uncliked value is "+d);
 return d;}
else if((b1==b3)&&(b3==b4)) { //alert("the uncliked value is "+b); 
return b;}
else if((b1==b2)&&(b2==b4)) {// alert("the uncliked value is "+c);
 return c;}
else if((b2==b3)&&(b3==b4)) {//alert("the uncliked value is "+a); 
 return a;}
else return 0;

}
	function get_win(num)
	{ 
		var num=num;
		
		var b1 = document.getElementById("b1").value;
		var b2 = document.getElementById("b2").value;
		var b3 = document.getElementById("b3").value;
		var b4 = document.getElementById("b4").value;
		var b5 = document.getElementById("b5").value;
		var b6 = document.getElementById("b6").value;
		var b7 = document.getElementById("b7").value;
		var b8 = document.getElementById("b8").value;
		var b9 = document.getElementById("b9").value;
		var b10 = document.getElementById("b10").value;
		var b11 = document.getElementById("b11").value;
		var b12 = document.getElementById("b12").value;
		var b13= document.getElementById("b13").value;
		var b14= document.getElementById("b14").value;
		var b15= document.getElementById("b15").value;
		var b16= document.getElementById("b16").value; 
		
  
      
		if ((b1==num) && (b2==num) && (b3==num) && (b4==num)){print_win(num);}
		else if ((b5==num) && (b6==num) && (b7==num) && (b8==num)){print_win(num);}
		else if ((b9==num) && (b10==num) && (b11==num) && (b12==num)){print_win(num);}
		else if ((b13==num) && (b14==num) && (b15==num) && (b16==num)){print_win(num);}
		else if ((b1==num) && (b5==num) && (b9==num) && (b13==num)){print_win(num);}
		else if ((b2==num) && (b6==num) && (b10==num) && (b14==num)){print_win(num);}
		else if ((b3==num) && (b7==num) && (b11==num) && (b15==num)){print_win(num);}
		else if ((b4==num) && (b8==num) && (b12==num) && (b16==num)){print_win(num);}
		else if ((b4==num) && (b7==num) && (b10==num) && (b13==num)){print_win(num);}
		else if ((b1==num) && (b6==num) && (b11==num) && (b16==num)){print_win(num);}
		} //  getwin() FUNCION ENDS HERE WITHOUT RETURNING NOTHING!!!

function find_index(a,b,c,d) 
{ // this function finds which three elements  are similar
	var a=a;
	var b=b;
	var c=c;
	var d=d;
	var index_a=b_array.indexOf(a);
	var index_b=b_array.indexOf(b);
	var index_c=b_array.indexOf(c);
	var index_d=b_array.indexOf(d);
	if ((index_a!=-1)&&(index_b!=-1)&&(index_c!=-1)&&(index_d!=-1)){ alert("all are  clicked!"); break;return 0;}
	else if ((index_a!=-1)&&(index_b!=-1)&&(index_c!=-1)) {alert("the uncliked buttton is  "+d);return d;}
	else if ((index_b!=-1)&&(index_c!=-1)&&(index_d!=-1)){alert("the uncliked buttton is  "+a);return a;}
	else if ((index_a!=-1)&&(index_c!=-1)&&(index_d!=-1)) {alert("the uncliked buttton is  "+b);return b;}
	else if ((index_a!=-1)&&(index_b!=-1)&&(index_d!=-1)) {alert("the uncliked buttton is  "+c);return c;}
	else return 0;

}

function print_win(num)// this function prints the winner result
	{
		var num=num;
		
		if (num==player1_symbol) {alert("Player "+player1+" Wins!! ");window.location.reload();}
		else if (num==player2_symbol) 

			{ 
				if(player2=='system') { alert("System Wins !!!!"); window.location.reload();}
				else { alert(" Player "+player2+" Wins!! ");  window.location.reload();}
	}
}


	