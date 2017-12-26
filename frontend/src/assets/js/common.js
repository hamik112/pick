$(function(){
	ImageHover();
	asideHeight();
	selectView();
	selectToggle();
	MaintabAction('.section_tab_widget', '.section_tab_contents', 'active');
	datePicker();
})

function asideHeight(){
	var _hei = $("body").height() -66;
	$("aside, .target_aside").css({height:_hei});
}
function adList(thisEl) {
	var $this = $(thisEl);
	var $showEl = $('.ad_list_category');
	$this.toggleClass('active');
	$showEl.toggle();
}

function adListClose() {
	var $btEl = $('#ad_list_cate');
	var $showEl = $('.ad_list_category');
	$btEl.removeClass('active');
	$showEl.hide();
}

function allCategory(thisEl) {
	var $this = $(thisEl);
	var $showEl = $('.setup_list');
	$this.toggleClass('active');
	$showEl.toggle();
}

function allCateClose() {
	var $btEl = $('#set_up');
	var $showEl = $('.setup_list');
	$btEl.removeClass('active');
	$showEl.hide();
}

//팝업 액션 전체
function popupActions(obj, layer, type, callLayer) {
	var $this = $(obj);
	var $layer = $('.' + layer);
	if(type == 'toggle') {
		$this.next('.' + layer).toggle();
	}else{
		//팝업 호출
		callLayer = callLayer + '.html';
		layerPop = '.' + layer;
		ajaxAppendCall('body', 'GET', callLayer, 'html', true, layerPopCallBack);
	}
}

//팝업 레이어 콜백
function layerPopCallBack() {
	var obj = $('.layer-pop-widget');
	var widget = $('.popup-widget');
	var closeBtn = $('.close_pop');

	var onOffDelay = 200;

	var appendPop = function() {
		obj.fadeIn(onOffDelay);
	};
	var removePop = function() {
		obj.fadeOut(onOffDelay);
		setTimeout(function() {
			obj.remove();
		},onOffDelay);
		scrollLock(false);
	};
	var popInnerStart = setTimeout(function() {
		popupInnerScroll();
	}, 300);

	//스크롤 고정
	appendPop();
	scrollLock(true);


	$(document).keyup(function(e) {
		if (e.keyCode == 27) {
			removePop();
		}
	});

	//윈도우창에 따른 스크롤 이벤트
	$(window).resize(function() {
		popupInnerScroll();
	});
	popInnerStart;


	closeBtn.click(function() {
		removePop();
		clearTimeout(popInnerStart);
	});

	tabAction('.tab-nav-widget', '.basic-tab-contents', 'active');
	googleTabAction('.analytics_tab_widget', '.analytics_tab_contents', 'active');
	ImageHover();
	selectView();
	CheckAll();
	ToggleClass();
	checkToggle();
	prologueView();
}

//팝업창 스크롤 자동 적용
function popupInnerScroll() {
	var widgetEl = $('.popup-widget');
	var widgetHeight = widgetEl.outerHeight(true);
	var windowHeight = $(window).height();
	var scrollClass = 'pop-scroll';
	if(widgetHeight > windowHeight) {
		widgetEl.addClass(scrollClass);
	}else{
		widgetEl.removeClass(scrollClass);
	}
}

//팝업 닫기 이벤트 제어
function layerClose(thisEl, lock, history) {
	var layerClass = 'layer-pop-widget';
	var obj = $(thisEl).parents('.' + layerClass);

	var onOffDelay = 200;

	var removePop = function() {
		obj.fadeOut(onOffDelay);
		setTimeout(function() {
			obj.remove();
		},onOffDelay);
	};


	removePop();

	if(history == true) {
		window.history.back();
	}
	if(lock == false) {
		scrollLock(lock);
	}
}

//팝업스크롤 락
function scrollLock(close) {
	var scrollPx = $(document).scrollTop();
	if(close === true) {
		$('body').addClass('default');
	}else if(close === false){
		$('body').removeClass('default');
	}
}

//append Functions
function ajaxAppendCall(id, type, dataUrl, dataType, async, callBack) {
	$.ajax({
		type: type ,
		url:dataUrl ,
		dataType : dataType,
		async:async,
		success: function(data) {
			$(id).parent('*').append(data);
			if(callBack !== undefined) {
				callBack();
			}
		},
		error:function() {
			alert('페이지를 읽을 수 없습니다.');
		}
	});
}

function tabAction(obj, contents, active) {
	$(obj).find("li").click(function() {
		var $this = $(this);
		var activeTab = $this.attr("rel");
		$(obj).find('li').removeClass(active);
		$this.addClass(active);
		$(contents).hide();
		$("#" + activeTab).show();
	});
}

function MaintabAction(obj, contents, active) {
	$(obj).find("li").click(function() {
		var $this = $(this);
		var activeTab = $this.attr("rel");
		$(obj).find('li').removeClass(active);
		$this.addClass(active);
		$(contents).hide();
		$("#" + activeTab).show();
	});
}

function googleTabAction(obj, contents, active) {
	$(obj).find("li").click(function() {
		var $this = $(this);
		var activeTab = $this.attr("rel");
		$(obj).find('li').removeClass(active);
		$this.addClass(active);
		$(contents).hide();
		$("#" + activeTab).show();
	});
}

function ImageHover(){
	$('#main_wrap ,.cate_contents').find('img').hover(function() {
		$(this).attr("src",$(this).attr("src").replace(/off\.jpg$/, 'on.jpg'));
	},
	function() {
		$(this).attr("src",$(this).attr("src").replace(/on\.jpg$/, 'off.jpg'));
	});
}

function selectView(){
	$(".select").on("click",function(e){
		e.stopPropagation();
		$(this).parent().find('p').addClass('arrow_up');
		var aactive = $(this).siblings('.select_view').hasClass("active");
		if(aactive == false){
				$(".select").siblings('.select_view').hide().removeClass('active');
				$(this).siblings('.select_view').show().addClass('active');
				$(this).parent().find('p').addClass('arrow_up');
		}else{
				$(this).siblings('.select_view').hide().removeClass('active');
				$(".select p").removeClass('arrow_up');
		}
	});

	// 셀렉트 박스 텍스트 넣기
	$(".select_view li").on("click",function(){
		$(this).parent().prev().find('p').text($(this).text());
		$(".select p").removeClass('arrow_up');
		$(".select_btn ul").hide();
		$('.select_view').removeClass('active');
	});
}

function CheckAll(){
	$("#all_check").click(function(){
		if($("#all_check").prop("checked")) {
			$("input[type=checkbox]").prop("checked",true);
		} else {
			$("input[type=checkbox]").prop("checked",false);
		}
	})
}

function selectToggle(){
	$('.test01').click(function(){
		$('.test01_view').toggle();
	})
}

function ToggleClass(){
	$(".cate_contents_widget li").click(function(){
		$(this).toggleClass("Click_on");
	});
}

function checkToggle(){
	$(".advertiser_search_result .result_check label").click(function(){
		$(this).parent().parent().toggleClass("result_on");
	});
}

function prologueView(){
	$(".prologue_area").on({
		mouseenter:function(){
			$(this).find(".prologue_view").show();
		},mouseleave:function(){
			$(this).find(".prologue_view").hide();
		}
	});
}
function datePicker(){
	$( "#datepicker1" ).datepicker({
		dateFormat: 'yy-mm-dd'
	});
};
