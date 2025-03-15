/**
 * 头疗SPA管理系统自定义 JavaScript
 */

// 初始化函数
function initAdmin() {
    // 全屏切换
    $('.fullscreen-btn').on('click', function(){
        var fullscreenElement = 
            document.fullscreenElement ||
            document.mozFullScreenElement ||
            document.webkitFullscreenElement ||
            document.msFullscreenElement;
        
        if (fullscreenElement) {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        } else {
            var element = document.documentElement;
            if (element.requestFullscreen) {
                element.requestFullscreen();
            } else if (element.mozRequestFullScreen) {
                element.mozRequestFullScreen();
            } else if (element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen();
            } else if (element.msRequestFullscreen) {
                element.msRequestFullscreen();
            }
        }
    });
    
    // 初始化表格
    if ($('.layui-table').length > 0) {
        layui.table.init('table-list', {
            height: 'full-220',
            limit: 20,
            page: true
        });
    }
    
    // 初始化表单
    if ($('.layui-form').length > 0) {
        layui.form.render();
    }
}

// 在 Layui 加载完成后初始化
layui.use(['element', 'layer', 'table', 'form', 'util'], function(){
    var $ = layui.jquery;
    
    // 初始化管理界面
    initAdmin();
});