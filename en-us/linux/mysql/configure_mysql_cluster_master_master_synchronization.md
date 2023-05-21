---
title: "Configuring MySQL Cluster with Master-Master Synchronization"
slug: Linux/Mysql/configure_mysql_cluster_master_master_synchronization
comments: true
category: mysql
tags:
  - High Availability
  - Cluster
  - MySQL
---

## Introduction

MySQL Cluster is a powerful feature in MySQL that allows for high availability and scalability by distributing the database across multiple servers. In this article, we will walk through the configuration steps for setting up a MySQL Cluster with master-master synchronization. We will assume the following server details for our setup:

MySQL Server1:
```
Server IP : 192.168.0.1
hostname  : mysqldb1
```
MySQL Server2:

```
Server IP : 192.168.0.2
hostname  : mysqldb2
```

## Configure MySQL Cluster
To configure MySQL Server for replication, add the following configuration under the mysqld context for each MySQL Server:

=== "MySQL1"

    ``` {.vim}
    [mysqld]

    bind-address        = 192.168.0.1
    server_id           = 1
    log_bin             = /var/log/mysql/mysql-bin.log
    log_bin_index       = /var/log/mysql/mysql-bin.log.index
    relay_log           = /var/log/mysql/mysql-relay-bin
    relay_log_index     = /var/log/mysql/mysql-relay-bin.index
    expire_logs_days    = 10
    max_binlog_size     = 100M
    log_slave_updates   = 1
    auto-increment-increment = 2
    auto-increment-offset = 1
    ```

=== "MySQL2"
    ``` {.vim}
    [mysqld]

    bind-address        = 192.168.0.2
    server_id           = 2
    log_bin             = /var/log/mysql/mysql-bin.log
    log_bin_index       = /var/log/mysql/mysql-bin.log.index
    relay_log           = /var/log/mysql/mysql-relay-bin
    relay_log_index     = /var/log/mysql/mysql-relay-bin.index
    expire_logs_days    = 10
    max_binlog_size     = 100M
    log_slave_updates   = 1
    auto-increment-increment = 2
    auto-increment-offset = 2
    ```

## Setting Up Replication

Next, we need to create a replica user on each server to establish replication. Run the following commands on MySQL Server1 and MySQL Server2, respectively:

=== "MySQL1"
    ``` {.console}
    mysql -uroot -p -e "GRANT REPLICATION SLAVE ON *.* TO 'replicauser'@'192.168.0.2' IDENTIFIED BY 'replica';"
    mysql -uroot -p -e "FLUSH PRIVILEGES;"
    ```

=== "MySQL2"
    ``` {.console}
    mysql -uroot -p -e "GRANT REPLICATION SLAVE ON *.* TO 'replicauser'@'192.168.0.1' IDENTIFIED BY 'replica';"
    mysql -uroot -p -e "FLUSH PRIVILEGES;"
    ```

## Restarting MariaDB Service

After creating the replica user, restart the MariaDB service on both servers to apply the configuration changes:

=== "MySQL1"

    ``` {.console}
    systemctl restart mariadb
    ```

=== "MySQL2"

    ``` {.console}
    systemctl restart mariadb
    ```

## Configuring Slave Replication

Now, we need to configure slave replication on both servers. Execute the following commands on each server:

=== "MySQL1"
    ``` {.mysql}
    STOP SLAVE;
    CHANGE MASTER TO master_host='192.168.0.2', master_port=3306, master_user='replicauser', master_password='replica', master_log_file='mysql-bin.000004', master_log_pos=3532;
    START SLAVE;
    ```

=== "MySQL2"
    ``` {.mysql}
    STOP SLAVE;
    CHANGE MASTER TO master_host='192.168.0.1', master_port=3306, master_user='replicauser', master_password='replica', master_log_file='mysql-bin.000002', master_log_pos=531;
    START SLAVE;
    SHOW MASTER STATUS;
    +------------------+----------+--------------+------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
    +------------------+----------+--------------+------------------+
    | mysql-bin.000004 |     3532 |              |                  |
    +------------------+----------+--------------+------------------+
    ```

## Data Synchronization
With the configuration and replication set up, any data created on either MariaDB server (MySQL Server1 or MySQL Server2) will be synchronized accordingly. The master-master synchronization ensures that changes made on one server are replicated to the other, allowing for high availability and data redundancy in the MySQL Cluster.

In this article, we have covered the essential steps to configure a MySQL Cluster with master-master synchronization. By following these steps, you can create a robust and scalable database environment for your applications.
