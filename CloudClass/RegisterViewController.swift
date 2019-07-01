//
//  RegisterViewController.swift
//  CloudClass
//  注册界面视图控制器
//  Created by 张雨帆 on 2019/6/25.
//  Copyright © 2019 张雨帆. All rights reserved.
//

import UIKit
import Alamofire


class RegisterViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    var autoCode = ""
    
    
    @IBOutlet var BackGround: UIView!
    @IBOutlet var ImageView: UIImageView!
    @IBOutlet var Nickname: UITextField! //昵称
    @IBOutlet var Email: UITextField! //邮箱
    @IBOutlet var Password: UITextField! //密码
    @IBOutlet var AutoCode: UITextField! //验证码
    
    // 获取验证码
    @IBAction func GetAutoCode(_ sender: UIButton) {
        AF.request("http://2547m30z96.wicp.vip:26056/register_code/?email=\(Email.text!)").responseString{ response in
            print(response.result)
            print(response.data!)
            print(response.value!)
            print(response.response!.statusCode)
            
            self.autoCode = response.value!
        }
    }
    
    // 注册
    @IBAction func Register(_ sender: UIButton) {
        if AutoCode.text! == autoCode {
            print("OK")
            let ChineseURL = "http://2547m30z96.wicp.vip:26056/register/?email=\(Email.text!)&user=\(Nickname.text!)&password=\(Password.text!)"
            let url = ChineseURL.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)
        AF.request(url!).responseString {
                response in
                print(response.result)
                print(response.data!)
                print(response.value!)
                print(response.response!.statusCode)
                if response.value! == "True" {
                    let alertController = UIAlertController(title: "注册成功，赶紧去登录吧～", message: nil, preferredStyle: .alert)
                    //显示提示框
                    self.present(alertController, animated: true, completion: nil)
                    //两秒钟后自动消失
                    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + 2) {
                        self.presentedViewController?.dismiss(animated: false, completion: nil)
                    }
                }
            }
        } else {
            let alertController = UIAlertController(title: "error: 验证码错误", message: nil, preferredStyle: .alert)
            //显示提示框
            self.present(alertController, animated: true, completion: nil)
            //两秒钟后自动消失
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + 2) {
                self.presentedViewController?.dismiss(animated: false, completion: nil)
            }
        }
        
    }
    
    
    // 修改头像
    @IBAction func ChangeTouxiang(_ sender: Any) {
        let imageVC = UIImagePickerController()
        imageVC.delegate = self
        imageVC.allowsEditing = true
        present(imageVC, animated: true, completion: nil)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        BackGround.layer.shadowColor = UIColor.black.cgColor
        BackGround.layer.shadowOffset = CGSize.init(width: 10, height: 10)
        BackGround.layer.shadowOpacity = 0.4
        BackGround.layer.shadowRadius = 10
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        var image: UIImage
        if picker.allowsEditing  {
            image = info[UIImagePickerController.InfoKey.editedImage] as! UIImage
        }
        else {
            image = info[UIImagePickerController.InfoKey.originalImage] as! UIImage
        }
        ImageView.image = image
        dismiss(animated: true, completion: nil)
    }
    

}
