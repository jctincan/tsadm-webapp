-- $Id: db-data.sql 12828 2015-05-05 23:38:31Z jrms $

-- slave hosts
INSERT INTO `host` (`id`, `fqdn`) VALUES (101, 'tsadm-node0');


-- sites
INSERT INTO `site` (`id`, `name`, `repo_uri`)
    VALUES (61001, 'regr', 'ssh://regr@tsadm-master:22/~/regr.git');
INSERT INTO `site` (`id`, `name`, `repo_uri`)
    VALUES (61002, 's0', 'ssh://s0@tsadm-master:22/~/s0.git');


-- sites envs
INSERT INTO `siteenv`
    (`id`, `site_id`, `name`, `host_id`) VALUES (5001, 61001, 'dev', 101);
INSERT INTO `siteenv`
    (`id`, `site_id`, `name`, `host_id`) VALUES (5002, 61001, 'test', 101);
INSERT INTO `siteenv`
    (`id`, `site_id`, `name`, `host_id`) VALUES (5004, 61002, 'dev', 101);


-- internal users (uid < 90)
INSERT INTO `user` VALUES (90, 'gitbot', 'BOT', 0.0);
INSERT INTO `user` VALUES (99, 'slavehost', 'HOST', 0.0);


-- users / developers (uid > 99)
INSERT INTO `user` VALUES (100, 'jeremias', 'ADMIN', 0.0);
INSERT INTO `user` VALUES (101, 'ibonelli', 'USER', 0.0);


-- users access control for envs
INSERT INTO `user_siteenv_acl` VALUES (100, 0);
INSERT INTO `user_siteenv_acl` VALUES (101, 5004);


-- user ssh keys
INSERT INTO `user_auth_keys` VALUES (0, 100, 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQ/mBHfR3T+7LwyYMv2CxGt0O8rV3P0K/pFB+YEmFKReK8G4p8HwK1C4UP1s5/6HN2byUZZJczUOT8VDmy4kmSNBiYZXyHiE7Cn9tCSQ926r8ykhjzU80xifEIcaWInCYQhwCRGtiS+TkucVhTY5uLdOa1xnGc9d5u8uk9U2+W9tQndBna/XHaD+5VhqLK4f+7nu2BkwemLuicR8uB2gPkbcOIvhAahrN6dplgwd4IE1ta4A8UeYTR+X/xzUAuddXFYoWWDmC+Y3c7AMecdioJ7EYNbFGt4UF4W0TusaIa74BmDqFK0TsDA8GBEdfUom04Al2IsZgPUcfd7h6SFj0H JRMS-KEY');
INSERT INTO `user_auth_keys` VALUES (1, 100, 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQ/mBHfR3T+7LwyYMv2CxGt0O8rV3P0K/pFB+YEmFKReK8G4p8HwK1C4UP1s5/6HN2byUZZJczUOT8VDmy4kmSNBiYZXyHiE7Cn9tCSQ926r8ykhjzU80xifEIcaWInCYQhwCRGtiS+TkucVhTY5uLdOa1xnGc9d5u8uk9U2+W9tQndBna/XHaD+5VhqLK4f+7nu2BkwemLuicR8uB2gPkbcOIvhAahrN6dplgwd4IE1ta4A8UeYTR+X/xzUAuddXFYoWWDmC+Y3c7AMecdioJ7EYNbFGt4UF4W0TusaIa74BmDqFK0TsDA8GBEdfUom04Al2IsZgPUcfd7h6SFj0H JRMS-KEY2');
INSERT INTO `user_auth_keys` VALUES (2, 101, 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQ/mBHfR3T+7LwyYMv2CxGt0O8rV3P0K/pFB+YEmFKReK8G4p8HwK1C4UP1s5/6HN2byUZZJczUOT8VDmy4kmSNBiYZXyHiE7Cn9tCSQ926r8ykhjzU80xifEIcaWInCYQhwCRGtiS+TkucVhTY5uLdOa1xnGc9d5u8uk9U2+W9tQndBna/XHaD+5VhqLK4f+7nu2BkwemLuicR8uB2gPkbcOIvhAahrN6dplgwd4IE1ta4A8UeYTR+X/xzUAuddXFYoWWDmC+Y3c7AMecdioJ7EYNbFGt4UF4W0TusaIa74BmDqFK0TsDA8GBEdfUom04Al2IsZgPUcfd7h6SFj0H IBONELLI-KEY');


-- tsadm internal
INSERT INTO `tsadm` (`dbversion`) VALUES (10000007);
