# 🗄️ Database Documentation

## 📚 Database Structure

### 1. SQLite Database (`sessions.db`)
**Location:** `./sessions.db`

#### Tables:

##### `sessions`
- `user_id` (TEXT) - Primary Key
- `session` (TEXT) - Session string
- `api_id` (INTEGER)
- `api_hash` (TEXT)
- `created_at` (TIMESTAMP)
- `last_used` (TIMESTAMP)

##### `markread_settings`
- `user_id` (TEXT) - Primary Key
- `pv` (BOOLEAN) - Mark read in private chats
- `group` (BOOLEAN) - Mark read in groups
- `channel` (BOOLEAN) - Mark read in channels

##### `muted_users`
- `id` (INTEGER) - Primary Key
- `owner_id` (TEXT)
- `user_id` (TEXT)
- `chat_id` (TEXT)
- `muted_at` (TIMESTAMP)

##### `user_credentials`
- `user_id` (TEXT) - Primary Key
- `api_id` (TEXT)
- `api_hash` (TEXT)
- `created_at` (TIMESTAMP)
- `last_updated` (TIMESTAMP)

### 2. MySQL Database (Coins System)
**Configuration:** Defined in `config.py`

#### Tables:

##### `user_coins`
- `user_id` (BIGINT UNSIGNED) - Primary Key
- `coins` (BIGINT) - Default: 0

##### `licenses`
- `code` (VARCHAR(64)) - Primary Key
- `user_id` (BIGINT UNSIGNED) - Foreign Key to user_coins
- `duration_months` (INT)
- `created_at` (TIMESTAMP)
- `used` (BOOLEAN) - Default: FALSE
- `redeemed_at` (TIMESTAMP) - Nullable
- `expires_at` (TIMESTAMP) - Nullable

## 🔄 Database Interactions

### Key Files and Their Database Operations

#### 1. `db.py`
- **Initialization**: Sets up SQLite database with connection pooling
- **Session Management**:
  - `get_session(user_id)` - Retrieve user session
  - `save_session(user_id, session, api_id, api_hash)` - Save/update session
  - `delete_session(user_id)` - Delete a session

- **MarkRead Settings**:
  - `get_markread_pv/group/channel(user_id)`
  - `set_markread_pv/group/channel(user_id, enabled)`

- **User Management**:
  - `add_muted_user(owner_id, user_id, chat_id)`
  - `remove_muted_user(owner_id, user_id, chat_id)`
  - `get_muted_users(owner_id, chat_id)`

- **File Operations**:
  - `register_new_file(file_data)`
  - `update_file_name(msg_id, new_name)`
  - `get_file_metadata(identifier)`

#### 2. `coins_db.py`
- **Coin Management**:
  - `get_coins(user_id)` - Get user's coin balance
  - `add_coins(user_id, amount)` - Add coins to user's balance
  - `deduct_coins(user_id, amount)` - Deduct coins from user's balance

- **License Management**:
  - `generate_license(user_id, duration_months)`
  - `redeem_license(code, user_id)`
  - `get_user_licenses(user_id)`

#### 3. `admin_coin.py`
- Admin-specific coin operations:
  - `add_coins_to_user(admin_id, user_id, amount)`
  - `get_all_balances()`
  - `generate_license_codes(admin_id, count, duration_months)`

## 🛠️ Database Setup

### SQLite Setup
No additional setup required. The database is automatically created on first run.

### MySQL Setup
1. Create a MySQL database:
   ```sql
   CREATE DATABASE botdata CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Create a user with appropriate permissions:
   ```sql
   CREATE USER 'botadmin'@'localhost' IDENTIFIED BY 'securepass';
   GRANT ALL PRIVILEGES ON botdata.* TO 'botadmin'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. Update `config.py` with your database credentials:
   ```python
   COIN_DB_CONFIG = {
       'host': '127.0.0.1',
       'port': 3306,
       'user': 'botadmin',
       'password': 'securepass',
       'db': 'botdata',
       'minsize': 5,
       'maxsize': 100,
       'autocommit': True,
   }
   ```

## 🔄 Database Migrations

### Adding New Tables
1. Add table creation SQL to `db.py` in the `_create_tables` method
2. Add any necessary indexes
3. The tables will be created on the next bot startup if they don't exist

### Schema Changes
1. Create a new migration file in `migrations/` with a timestamp
2. Include both `up()` and `down()` methods
3. Test the migration thoroughly before applying to production

## 🔒 Security Considerations

1. **Connection Pooling**:
   - Uses SQLAlchemy's connection pooling
   - Configured with min/max connections in `config.py`

2. **Sensitive Data**:
   - API keys and hashes are stored encrypted
   - Session strings are stored securely

3. **Backup**:
   - Regular backups of both SQLite and MySQL databases recommended
   - Consider using `mysqldump` for MySQL backups
   - For SQLite, simply copy the database file when the bot is not running

## 📊 Performance Optimization

1. **Indexing**:
   - All primary keys are automatically indexed
   - Foreign keys are indexed where appropriate
   - Consider adding indexes for frequently queried columns

2. **Caching**:
   - Implements in-memory caching for frequently accessed data
   - Cache invalidation on updates

3. **Connection Management**:
   - Uses connection pooling to minimize connection overhead
   - Connections are properly closed after use

## 🐛 Troubleshooting

### Common Issues
1. **Connection Errors**:
   - Verify database server is running
   - Check credentials in `config.py`
   - Ensure the database user has correct permissions

2. **Performance Issues**:
   - Check for missing indexes
   - Monitor connection pool usage
   - Optimize slow queries

3. **Data Corruption**:
   - Restore from backup if available
   - For SQLite, run `VACUUM` to rebuild the database file

## 📝 License
This database documentation is part of the SelfSaz Bot project and is licensed under the MIT License.
