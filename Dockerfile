# Um Dockerfile para os tres executaveis Java. O modulo entra por argumento,
# e nao por copia-e-cola: tres arquivos identicos divergiriam em silencio na
# primeira vez que alguem editasse um so.
#
# O reactor inteiro e construido de uma vez porque os tres dependem de
# `shared`, e o Maven precisa dele instalado para resolver a dependencia.
ARG JAVA_VERSION=25

FROM maven:3.9-eclipse-temurin-${JAVA_VERSION} AS build
WORKDIR /build

# As dependencias entram numa camada propria: elas mudam muito menos que o
# codigo, e o cache do Docker so e reaproveitado se as camadas estaveis vierem
# antes das volateis.
COPY pom.xml .
COPY shared/pom.xml shared/
COPY lab-plane/pom.xml lab-plane/
COPY lab-journal/pom.xml lab-journal/
COPY system-under-test/pom.xml system-under-test/
RUN mvn -B -q dependency:go-offline

COPY shared/src shared/src
COPY lab-plane/src lab-plane/src
COPY lab-journal/src lab-journal/src
COPY system-under-test/src system-under-test/src
RUN mvn -B -q -DskipTests package

FROM eclipse-temurin:${JAVA_VERSION}-jre-alpine AS runtime
ARG MODULE
RUN test -n "${MODULE}" || (echo "MODULE e obrigatorio" && exit 1)

# O processo nao roda como root. Um experimento da etapa 6 mata processos de
# proposito, e um deles com privilegio no host e superficie desnecessaria.
RUN addgroup -S lab && adduser -S -G lab lab
USER lab

WORKDIR /app
COPY --from=build /build/${MODULE}/target/${MODULE}-*.jar app.jar

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
