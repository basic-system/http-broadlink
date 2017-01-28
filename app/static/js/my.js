// copy from https://quato.com.ua/ajax-redaktirovanie-tablic-i-tablichnyx-dannyx/
		//при нажатии на ячейку таблицы с классом edit
		$(document).on('click', 'td.edit', function(){
			//находим input внутри элемента с классом ajax и вставляем вместо input его значение
			$('.ajax').html($('.ajax input').val());
			//удаляем все классы ajax
			$('.ajax').removeClass('ajax');
			//Нажатой ячейке присваиваем класс ajax
			$(this).addClass('ajax');
			//внутри ячейки создаём input и вставляем текст из ячейки в него
			$(this).html('<input id="editbox" size="'+ $(this).text().length+'" value="' + $(this).text() + '" type="text">');
			//устанавливаем фокус на созданном элементе
			$('#editbox').focus();
			// var el=document.getElementById(‘editbox’);
			// el.focus();
			// el.setSelectionRange(el.value.length,el.value.length);
		});

		//определяем нажатие кнопки на клавиатуре
		$(document).on('keydown', 'td.edit', function(event){
		//получаем значение класса и разбиваем на массив
		//в итоге получаем такой массив - arr[0] = edit, arr[1] = наименование столбца, arr[2] = id строки
		arr = $(this).attr('class').split( " " );
		//проверяем какая была нажата клавиша и если была нажата клавиша Enter (код 13)
		   if(event.which == 13)
		   {
				//получаем наименование таблицы, в которую будем вносить изменения
				var table = $('table').attr('id');
				//выполняем ajax запрос методом POST
				$.ajax({ type: "POST",
				//в файл update_cell.php
				url:"/edit_name",
				//создаём строку для отправки запроса
				//value = введенное значение
				//id = номер строки
				//field = название столбца
				//table = собственно название таблицы
				 data: "value="+$('.ajax input').val()+"&mac="+arr[2],
				//при удачном выполнении скрипта, производим действия
				 success: function(data){
				//находим input внутри элемента с классом ajax и вставляем вместо input его значение
				 $('.ajax').html($('.ajax input').val());
				//удаялем класс ajax
				 $('.ajax').removeClass('ajax');
				 }});
		 	}

		});

		//Сохранение при нажатии вне поля
		$(document).on('blur', '#editbox', function(){

				var arr = $('td.ajax').attr('class').split( " " );
				//получаем наименование таблицы, в которую будем вносить изменения
				var table = $('table').attr('id');
				//выполняем ajax запрос методом POST
				$.ajax({ type: "POST",
				//в файл update_cell.php
				url:"/edit_name",
				//создаём строку для отправки запроса
				//value = введенное значение
				//id = номер строки
				//field = название столбца
				//table = собственно название таблицы
				 data: "value="+$('.ajax input').val()+"&mac="+arr[2],
				//при удачном выполнении скрипта, производим действия
				 success: function(data){
				//находим input внутри элемента с классом ajax и вставляем вместо input его значение
				 $('.ajax').html($('.ajax input').val());
				//удаялем класс ajax
				 $('.ajax').removeClass('ajax');
				 }});
		});


		$(document).on('change', 'input.checkbox', function(){
			var arr = $(this).attr('class').split( " " );
			if ( this.checked ) {
				console.log("enable");
				$.ajax({ type: "POST",
				//в файл update_cell.php
				url:"/switch",
				//создаём строку для отправки запроса
				//value = введенное значение
				//id = номер строки
				//field = название столбца
				//table = собственно название таблицы
				 data: "mac="+arr[1]+"&action=on",
				});
			} else {
				console.log("disable");
				$.ajax({ type: "POST",
				//в файл update_cell.php
				url:"/switch",
				//создаём строку для отправки запроса
				//value = введенное значение
				//id = номер строки
				//field = название столбца
				//table = собственно название таблицы
				 data: "mac="+arr[1]+"&action=off",
				});
			}});

		$(document).on('click', 'td.remove', function(){
			var arr = $(this).attr('class').split( " " );
			$.ajax({ type: "POST",
			//в файл update_cell.php
			url:"/remove",
			//создаём строку для отправки запроса
			//value = введенное значение
			//id = номер строки
			//field = название столбца
			//table = собственно название таблицы
			 data: "mac="+arr[1],
			});
		});

		$(document).on('click', 'a.add_rm', function() {
			var arr = $(this).attr('class').split(" ");
			$.ajax({ type: "POST",
				url:"/add_rm_device",
				data: "mac="+arr[1],
				success: function(data){
					// $('.ajax').html($('.ajax input').val());
						console.log(data);
						$("#common_table tbody").append("\
					<tr>\
						<td></td>\
						<td></td>\
						<td class=\"editrm "+data['name']+"\">"+data['name']+"</td>\
						<td>\
							<div class=\"pull-right\"><a href=\"#\" class=\"add_button "+data['name']+"\">Learn</a>\
						</td>\
					</tr>");
					}
			});
		});

		$(document).on('click', 'td.editrm', function(){
			$('.ajax').html($('.ajax input').val());
			$('.ajax').removeClass('ajax');
			$(this).addClass('ajax');
			$(this).html('<input id="editbox" size="'+ $(this).text().length+'" value="' + $(this).text() + '" type="text">');
			$('#editbox').focus();
		});

		$(document).on('keydown', 'td.editrm', function(event){
		arr = $(this).attr('class').split( " " );
		   if(event.which == 13)
		   {
				var table = $('table').attr('id');
				$.ajax({ type: "POST",
				url:"/editrm_name",
				 data: "value="+$('.ajax input').val()+"&mac="+arr[1]+"&name="+arr[2],
				 success: function(data){
				 $('.ajax').html($('.ajax input').val());
				 $('.ajax').removeClass('ajax');
				 }});
		 	}

		});

		$(document).on('blur', '#editbox', function(){

				var arr = $('td.ajax').attr('class').split( " " );
				var table = $('table').attr('id');
				$.ajax({ type: "POST",
				url:"/editrm_name",
				 data: "value="+$('.ajax input').val()+"&mac="+arr[1]+"&name="+arr[2],
				 success: function(data){
				 $('.ajax').html($('.ajax input').val());
				 $('.ajax').removeClass('ajax');
				 }});
		});


		$(document).on('click', 'a.add_button', function() {
			var arr = $(this).attr('class').split(" ");
			console.log('add_button pressed');
			$.ajax({ type: "POST",
				url:"/add_button",
				data: "device="+arr[1],
				success: function(data){
					// $('.ajax').html($('.ajax input').val());
						console.log(data);
					}
			});
		});

		$(document).on('click', 'a.press_button', function() {
			var arr = $(this).attr('class').split(" ");
			console.log('press_button pressed');
			console.log(arr);
			$.ajax({ type: "POST",
				url:"/press_button",
				data: "mac="+arr[1]+"&device="+arr[2]+"&name="+arr[3],
				success: function(data){
					// $('.ajax').html($('.ajax input').val());
						console.log(data);
					}
			});
		});
