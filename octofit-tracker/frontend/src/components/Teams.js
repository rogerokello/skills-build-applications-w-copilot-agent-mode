import React, { useEffect, useState } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    fetch('https://zany-goldfish-q7gqgjvg9q739rxj-8000.app.github.dev/api/teams')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          console.log('Fetched teams:', data); // Debugging line
          setTeams(data);
        } else {
          console.error('Expected an array but received:', data);
        }
      })
      .catch(error => console.error('Error fetching teams:', error));
  }, []);

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">Teams</h1>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Team Name</th>
            <th>Members</th>
          </tr>
        </thead>
        <tbody>
          {teams.map((team, index) => (
            <tr key={team._id || index}>
              <td>{team.name}</td>
              <td>
                <ul>
                  {team.members.map((member, memberIndex) => (
                    <li key={member._id || memberIndex}>{member.username} ({member.email})</li>
                  ))}
                </ul>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Teams;
