//
//  LoginViewController.swift
//  CloudClass
//  登陆界面视图控制器
//  Created by 张雨帆 on 2019/6/24.
//  Copyright © 2019 张雨帆. All rights reserved.
//


import UIKit
import Alamofire


class LoginViewController: UIViewController {
    
    var UserName = "这是默认名"
    var UserType = "我什么也不是"
    
    @IBOutlet var BackGround: UIView!
    @IBOutlet var Account: UITextField! //账号（邮箱or电话）
    @IBOutlet var Password: UITextField! //密码
    @IBAction func Login(_ sender: UIButton) {
        
        AF.request("http://2547m30z96.wicp.vip:26056/login/?email=\(Account.text!)&password=\(Password.text!)").responseJSON { response in
            let data = response.value! as! NSDictionary
            let statusCode = data["statusCode"] as! Int
            if statusCode == 0 {
                self.UserName = data["username"] as! String
                self.UserType = data["usertype"] as! String
                self.performSegue(withIdentifier: "Login", sender: sender)
            } else {
                let WrongInfo = data["errorDetail"] as! String
                let alertController = UIAlertController(title: WrongInfo, message: nil, preferredStyle: .alert)
                //显示提示框
                self.present(alertController, animated: true, completion: nil)
                //两秒钟后自动消失
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + 2) {
                    self.presentedViewController?.dismiss(animated: false, completion: nil)
                }
            }
        }
    }
    
    // 设置手动跳转登录按钮动作
    override func shouldPerformSegue(withIdentifier identifier: String, sender: Any?) -> Bool {
        if identifier == "Login" {
            return false
        }
        return true
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        BackGround.layer.shadowColor = UIColor.black.cgColor
        BackGround.layer.shadowOffset = CGSize.init(width: 10, height: 10)
        BackGround.layer.shadowOpacity = 0.4
        BackGround.layer.shadowRadius = 10
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier! == "Login" {
            print(UserName)
            FirstViewController.UserName = UserName
            FirstViewController.UserType = UserType
        }
    }
    
}
