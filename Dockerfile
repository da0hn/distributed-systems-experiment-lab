# Um Dockerfile para todos os executáveis Java. O módulo entra por argumento,
# e não por copia-e-cola: arquivos idênticos divergiriam em silêncio na
# primeira vez que alguém editasse um só.
#
# Constrói `shared` e depois **apenas** o módulo pedido. Antes o reactor
# inteiro era construído uma vez por imagem, e uma mudança em qualquer `src/`
# invalidava a camada de compilação de todas.
ARG JAVA_VERSION=25

FROM maven:3.9-eclipse-temurin-${JAVA_VERSION} AS build
WORKDIR /build

# As dependências entram numa camada própria: elas mudam muito menos que o
# código, e o cache do Docker só é reaproveitado se as camadas estáveis vierem
# antes das voláteis. Os cinco `pom.xml` de módulo entram porque o Maven
# precisa do reactor completo para resolver o parent e o agregador.
COPY pom.xml .
COPY shared/pom.xml shared/
COPY api-gateway/pom.xml api-gateway/
COPY lab-plane/pom.xml lab-plane/
COPY lab-journal/pom.xml lab-journal/
COPY system-under-test/pom.xml system-under-test/
RUN mvn -B -q dependency:go-offline

# `shared` vem antes, e sozinho. Nenhum executável depende de outro, então
# esta camada é idêntica em todas as imagens e sobrevive a qualquer mudança em
# `lab-plane/`, `lab-journal/`, `system-under-test/` ou `api-gateway/`. O
# `install` o publica no `~/.m2` local da camada, que é como o `package`
# seguinte resolve a dependência sem `-am`.
COPY shared/src shared/src
RUN mvn -B -q -pl shared -am -DskipTests install

# Só agora entra o código do módulo pedido. É a primeira camada que difere
# entre as quatro imagens Java, e é de propósito que ela seja a última.
ARG MODULE
RUN test -n "${MODULE}" || (echo "MODULE é obrigatório" && exit 1)
COPY ${MODULE}/src ${MODULE}/src
RUN mvn -B -q -pl ${MODULE} -DskipTests package

FROM eclipse-temurin:${JAVA_VERSION}-jre-alpine AS runtime
ARG MODULE

# O processo não roda como root. Um experimento da etapa 6 mata processos de
# propósito, e um deles com privilégio no host é superfície desnecessária.
RUN addgroup -S lab && adduser -S -G lab lab
USER lab

WORKDIR /app
COPY --from=build /build/${MODULE}/target/${MODULE}-*.jar app.jar

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
