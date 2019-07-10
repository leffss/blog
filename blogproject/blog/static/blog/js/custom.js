
/* 返回顶部 */
$(function(){
	// $(".gototop").gototop();
	$(".gototop").gototop({
		position : 0,
		duration : 850,		/* 滚动时间，越小越快 */
		visibleAt : 300, 	/* 向下滚动多少像素后出现返回顶部按钮 */
		classname : "isvisible"
	});
});

