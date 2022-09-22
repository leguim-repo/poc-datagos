docker run \
    -ti \
    --rm \
    --link sonarqube \
    -e SONAR_HOST_URL="http://172.17.0.2:9000/" \
    -e SONAR_LOGIN="sqp_8074a737fb05a8488f5881227b3692c915e1d78d" \
    -v "/Users/miguel/Desktop/Repositorios/leguim-repo/poc-datagos:/usr/src" \
    sonarsource/sonar-scanner-cli -X

