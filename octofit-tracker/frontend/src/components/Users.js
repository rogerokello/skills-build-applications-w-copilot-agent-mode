import React, { useEffect, useState } from 'react';

function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('https://zany-goldfish-q7gqgjvg9q739rxj-8000.app.github.dev/api/users')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          setUsers(data);
        } else {
          console.error('Expected an array but received:', data);
        }
      })
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">Users</h1>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, index) => (
            <tr key={user._id || index}>
              <td>{user.username}</td>
              <td>{user.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Users;
