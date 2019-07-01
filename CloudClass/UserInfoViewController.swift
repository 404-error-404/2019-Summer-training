//
//  SecondViewController.swift
//  CloudClass
//
//  Created by 张雨帆 on 2019/6/24.
//  Copyright © 2019 张雨帆. All rights reserved.
//

import UIKit

class UserInfoViewController: UIViewController {

    
    @IBOutlet var UserName: UILabel!
    @IBOutlet var UserType: UILabel!
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.navigationController?.setNavigationBarHidden(true, animated: true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        UserName.text = FirstViewController.UserName
        UserType.text = FirstViewController.UserType
    }


}

