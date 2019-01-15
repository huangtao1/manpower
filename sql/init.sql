#初始化数据库信息脚本
-- ----------------------------
-- Records of dms_menu
-- ----------------------------
INSERT INTO `dms_menu` VALUES ('1', '系统管理', null, 'icon-compass', '1', '系统管理', '1', '1', null);
INSERT INTO `dms_menu` VALUES ('2', '菜单管理', 'manager.show_menus', null, '2', '管理菜单页面', '1', '0', '1');
INSERT INTO `dms_menu` VALUES ('3', '账户管理', 'manager.accounts_manage', null, '1', '账户管理页面', '1', '0', '1');
INSERT INTO `dms_menu` VALUES ('4', '角色管理', 'manager.role_manage', null, '3', '角色管理页面', '1', '0', '1');
INSERT INTO `dms_menu` VALUES ('5', '系统参数管理', 'manager.system_para', null, '4', '管理系统参数', '1', '0', '1');
INSERT INTO `dms_menu` VALUES ('6', '组织架构管理', 'manager.show_organize', null, '5', '管理组织架构页面', '1', '0', '1');

-- ----------------------------
-- Records of dms_role
-- ----------------------------
INSERT INTO `dms_role` VALUES ('1', 'admin', 'manager.accounts_manage', '1,2,3,4,5,6');
