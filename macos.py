import psutil
import AppKit
import Quartz
import CoreFoundation


def get_installed_application(app_name):
    # 获取 /Applications 目录下的所有应用程序
    applications_dir = "/Applications"
    all_app, _ = AppKit.NSFileManager.defaultManager().contentsOfDirectoryAtPath_error_(applications_dir, None)
    for app_path in all_app:
        full_path = f"{applications_dir}/{app_path}"
        if full_path.endswith('.app'):
            bundle = AppKit.NSBundle.bundleWithPath_(full_path)
            if not bundle:
                continue
            bundle_id = bundle.infoDictionary().get('CFBundleName', '')
            if bundle_id == app_name:
                return bundle

    return None


def find_running_application_pid(app_name=None, pid=None):
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        # print(proc.info)
        if proc.info['name'] == app_name:
            return proc.info['pid']
    return 0


def run_event_loop_briefly(duration=0.01, iterations=5):
    """短暂运行 Cocoa 的事件循环。"""
    for _ in range(iterations):
        CoreFoundation.CFRunLoopRunInMode(
            CoreFoundation.kCFRunLoopDefaultMode,
            duration,
            False
        )

def find_running_application(app_name=None, pid=None):
    """查找正在运行的应用程序，可按名称或 PID 查找。"""
    workspace = Quartz.NSWorkspace.sharedWorkspace()

    # 在获取应用程序列表之前短暂运行事件循环
    run_event_loop_briefly()

    for app in workspace.runningApplications():
        if pid and app.processIdentifier() == pid:
            return app
        if app_name and app.localizedName() == app_name:
            return app
        # 如果 localizedName 不匹配，尝试使用 bundle 的 CFBundleName
        try:
            bundle_url = app.bundleURL()
            if bundle_url:
                bundle_path = bundle_url.path()
                bundle = AppKit.NSBundle.bundleWithPath_(bundle_path)
                if bundle:
                    bundle_name = bundle.infoDictionary().get('CFBundleName', '')
                    if app_name and bundle_name == app_name:
                        return app
        except Exception as e:
            print(f"Error accessing bundle info for {app.localizedName()}: {e}")
            continue
    return None


def move_window_foreground(app_name=None, pid=None):
    if app_name in ["战网"]:
        app_name = "Battle.net"
    elif app_name in ["炉石传说"]:
        app_name = "Hearthstone"
    workspace = AppKit.NSWorkspace.sharedWorkspace()
    application = find_running_application(app_name, pid)
    if not application:
        application = get_installed_application(app_name)
    bundle_identifier = application.bundleIdentifier()
    url = workspace.URLForApplicationWithBundleIdentifier_(bundle_identifier)

    if url:
        workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([url], bundle_identifier, 0, None, None)


def get_window_rect(pid):
    """
    获取应用程序窗口的位置和大小
    返回 (left, top, right, bottom) 坐标
    """

    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)
    for window in windows:
        window_pid = int(window['kCGWindowOwnerPID'])
        if not window_pid == pid:
            continue
        bounds = window.get('kCGWindowBounds')
        # print(bounds)
        left = bounds['X']
        top = bounds['Y']
        right = left + bounds['Width']
        bottom = top + bounds['Height']
        return left, top, right, bottom


# 示例用法
if __name__ == "__main__":
    # take_snapshot()
    # a = move_window_foreground('Hearthstone')
    # print(find_running_application('Hearthstone'))
    # a = get_installed_application('Battle.net')
    # a = find_running_application('Hearthstone')
    # move_window_foreground(pid=9888)
    print(get_window_rect(14391))